#!/usr/bin/env python3
"""Reproduce VL08's MotionSense classroom model and figures.

Run from the repository root with Python 3, NumPy and Matplotlib:
    python3 code/vl08_activity_demo.py

The model is a deliberately small, actually trained Float32 export, not a
validated activity-recognition product or a measured embedded implementation.
Data attribution and the upstream MIT license are stored beside the CSV.
"""
from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
import platform

# Small deterministic classroom matrices do not need a threaded BLAS.
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/08_motion_sense"
FIGURES = ROOT / "assets/figures/08_ki_beschleuniger_edge_ai/revision"
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".quarto/cache/vl08-matplotlib"))
os.environ.setdefault("XDG_CACHE_HOME", str(ROOT / ".quarto/cache"))
CLASSES = ("standing", "walking", "jogging")
LABELS = ("Stehen", "Gehen", "Laufen")
COLORS = ("#1D1D1F", "#C50018", "#245B78")
MARKERS = ("o", "^", "s")
SEED = 20261117
EPOCHS = 600
BATCH_SIZE = 64
LEARNING_RATE = 0.003
WINDOW = 32
SAMPLE_HZ = 50


def load_windows():
    groups = {}
    source = DATA / "motionsense-activities.csv"
    with source.open(newline="", encoding="utf-8") as stream:
        for row in csv.DictReader(stream):
            key = (int(row["subject"]), row["activity"])
            groups.setdefault(key, []).append(
                (int(row["sample"]), [float(row[k]) for k in ("x", "y", "z")])
            )
    assert len(groups) == 24 * 3
    samples, targets, subjects, local_windows = [], [], [], []
    raw = {}
    for subject in range(1, 25):
        for label, activity in enumerate(CLASSES):
            values = sorted(groups[(subject, activity)])
            indices = [v[0] for v in values]
            assert len(values) == 512
            assert np.all(np.diff(indices) == 1)
            signal = np.asarray([v[1] for v in values], dtype=np.float64)
            assert signal.shape == (512, 3) and np.isfinite(signal).all()
            raw[(subject, activity)] = signal
            for start in range(0, len(signal), WINDOW):
                samples.append(signal[start : start + WINDOW])
                targets.append(label)
                subjects.append(subject)
                local_windows.append(start // WINDOW)
    windows = np.asarray(samples)
    assert windows.shape == (1152, 32, 3)
    return windows, np.asarray(targets), np.asarray(subjects), np.asarray(local_windows), raw


def logits(x, parameters):
    w1, b1, w2, b2 = parameters
    hidden = np.maximum(0, x @ w1.T + b1)
    return hidden @ w2.T + b2


def measure(x, labels, parameters):
    scores = logits(x, parameters)
    centered = scores - scores.max(axis=1, keepdims=True)
    # Stable log-sum-exp avoids taking log(0) after Float32 underflow.
    log_denominator = np.log(np.exp(centered).sum(axis=1))
    loss = (log_denominator - centered[np.arange(len(labels)), labels]).mean()
    prediction = scores.argmax(axis=1)
    confusion = np.zeros((3, 3), dtype=int)
    np.add.at(confusion, (labels, prediction), 1)
    return {"loss": float(loss), "accuracy": float((prediction == labels).mean()),
            "confusion_rows_true_columns_predicted": confusion.tolist()}


def train_model(x, y, masks):
    rng = np.random.default_rng(SEED)
    train = masks["train"]
    mean = x[train].mean(axis=0)
    std = x[train].std(axis=0)
    std = np.maximum(std, 1e-6)
    normalized = (x - mean) / std
    train_x, train_y = normalized[train], y[train]
    parameters = [rng.normal(0, np.sqrt(2 / 96), (16, 96)), np.zeros(16),
                  rng.normal(0, np.sqrt(2 / 16), (3, 16)), np.zeros(3)]
    moments = [np.zeros_like(p) for p in parameters]
    velocities = [np.zeros_like(p) for p in parameters]
    history = []
    step = 0
    # Architecture, epoch count and learning rate are fixed before inspecting test data.
    # The validation curve is recorded; no checkpoint is selected from it.
    for epoch in range(EPOCHS + 1):
        if epoch % 10 == 0:
            train_result = measure(normalized[train], y[train], parameters)
            val = masks["validation"]
            val_result = measure(normalized[val], y[val], parameters)
            history.append({"epoch": epoch, "train_loss": train_result["loss"],
                            "validation_loss": val_result["loss"]})
        if epoch == EPOCHS:
            break
        order = rng.permutation(len(train_x))
        for begin in range(0, len(order), BATCH_SIZE):
            rows = order[begin : begin + BATCH_SIZE]
            batch, target = train_x[rows], train_y[rows]
            w1, b1, w2, b2 = parameters
            preactivation = batch @ w1.T + b1
            hidden = np.maximum(0, preactivation)
            scores = hidden @ w2.T + b2
            scores -= scores.max(axis=1, keepdims=True)
            derivative = np.exp(scores)
            derivative /= derivative.sum(axis=1, keepdims=True)
            derivative[np.arange(len(rows)), target] -= 1
            derivative /= len(rows)
            gradient_w2 = derivative.T @ hidden
            gradient_b2 = derivative.sum(axis=0)
            hidden_derivative = derivative @ w2
            hidden_derivative[preactivation <= 0] = 0
            gradient_w1 = hidden_derivative.T @ batch
            gradient_b1 = hidden_derivative.sum(axis=0)
            step += 1
            for i, gradient in enumerate((gradient_w1, gradient_b1, gradient_w2, gradient_b2)):
                moments[i] = 0.9 * moments[i] + 0.1 * gradient
                velocities[i] = 0.999 * velocities[i] + 0.001 * gradient * gradient
                first = moments[i] / (1 - 0.9 ** step)
                second = velocities[i] / (1 - 0.999 ** step)
                parameters[i] -= LEARNING_RATE * first / (np.sqrt(second) + 1e-8)
    # Publish and evaluate the exported Float32 representation, including normalization.
    exported = [p.astype(np.float32) for p in parameters]
    mean32, std32 = mean.astype(np.float32), std.astype(np.float32)
    normalized32 = (x.astype(np.float32) - mean32) / std32
    metrics = {name: measure(normalized32[mask], y[mask], exported)
               for name, mask in masks.items()}
    return exported, mean32, std32, normalized32, metrics, history


def save_json(filename, value):
    path = DATA / filename
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def configure_plots():
    Path(os.environ["MPLCONFIGDIR"]).mkdir(parents=True, exist_ok=True)
    Path(os.environ["XDG_CACHE_HOME"]).mkdir(parents=True, exist_ok=True)
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 18,
        "axes.titlesize": 19, "axes.labelsize": 18,
        "xtick.labelsize": 15, "ytick.labelsize": 15,
        "legend.fontsize": 16, "text.color": "#1D1D1F",
        "axes.labelcolor": "#1D1D1F", "xtick.color": "#1D1D1F",
        "ytick.color": "#1D1D1F", "axes.edgecolor": "#656D76",
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.facecolor": "white", "figure.facecolor": "white",
        "grid.color": "#D7DADF", "grid.linewidth": 0.7,
        "svg.hashsalt": "mct3-vl08-activity-demo",
    })
    return plt


def save_figure(fig, name):
    FIGURES.mkdir(parents=True, exist_ok=True)
    svg_path = FIGURES / f"{name}.svg"
    fig.savefig(svg_path, bbox_inches="tight", metadata={"Date": None})
    # Normalize trailing blanks in Matplotlib's multi-line SVG paths.
    svg_path.write_text("\n".join(line.rstrip() for line in svg_path.read_text().splitlines()) + "\n",
                        encoding="utf-8")
    fig.savefig(FIGURES / f"{name}.png", dpi=180, bbox_inches="tight",
                metadata={"Software": "MCT3 reproducible activity demo"})


def make_figures(windows, labels, subjects, raw, history):
    plt = configure_plots()
    # One preselected person is shown for all activities; raw magnitude includes gravity.
    fig, axes = plt.subplots(3, 1, figsize=(11.5, 6.0), sharex=True, sharey=True,
                             layout="constrained")
    t = np.arange(512) / SAMPLE_HZ
    for k, activity in enumerate(CLASSES):
        magnitude = np.linalg.norm(raw[(1, activity)], axis=1)
        axes[k].plot(t, magnitude, color=COLORS[k], linewidth=1.65)
        axes[k].text(0.015, 0.84, LABELS[k], transform=axes[k].transAxes,
                     fontsize=18, weight="bold", bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.9})
        axes[k].grid(axis="y", alpha=0.6)
    axes[-1].set_xlabel("Zeit im Ausschnitt [s]")
    fig.supylabel(r"Beschleunigungsbetrag $|a|$ [g]", fontsize=18)
    save_figure(fig, "traces")
    plt.close(fig)

    magnitude = np.linalg.norm(windows, axis=2)
    features = np.column_stack((magnitude.mean(axis=1), magnitude.std(axis=1)))
    fig, ax = plt.subplots(figsize=(10.6, 5.6), layout="constrained")
    for k in range(3):
        choose = labels == k
        ax.scatter(features[choose, 0], features[choose, 1], c=COLORS[k],
                   marker=MARKERS[k], s=27, alpha=0.65, label=LABELS[k], linewidths=0)
    ax.set_xlabel(r"Mittelwert von $|a|$ je Fenster [g]")
    ax.set_ylabel(r"Standardabweichung von $|a|$ [g]")
    ax.legend(frameon=False, markerscale=1.4)
    ax.grid(alpha=0.5)
    save_figure(fig, "features")
    plt.close(fig)

    train = subjects <= 16
    feature_mean = features[train].mean(axis=0)
    feature_std = features[train].std(axis=0)
    scaled = (features - feature_mean) / feature_std
    limits = (min(-2.0, float(scaled.min()) - 0.15), max(3.0, float(scaled.max()) + 0.15))
    # Show a useful central view while keeping source feature values in model-summary.json.
    low, high = max(-2.5, limits[0]), min(5.0, limits[1])
    line_x = np.linspace(low, high, 200)
    fig, axes = plt.subplots(1, 2, figsize=(12.2, 5.2), sharex=True, sharey=True,
                             layout="constrained")
    for ax in axes:
        ax.scatter(scaled[:, 0], scaled[:, 1], color="#656D76", s=8, alpha=0.8, linewidths=0)
        ax.set_xlim(low, high)
        ax.set_ylim(low, high)
        ax.axhline(0, color="#656D76", linewidth=0.7)
        ax.axvline(0, color="#656D76", linewidth=0.7)
        ax.set_xlabel(r"$x_1$: standardisierter Mittelwert")
        ax.grid(alpha=0.4)
    axes[0].set_ylabel(r"$x_2$: standardisierte Streuung")
    for angle, color, style in [(135, "#1D1D1F", "--"), (110, "#C50018", "-")]:
        phi = np.deg2rad(angle)
        y = -(np.cos(phi) * line_x) / np.sin(phi)
        axes[0].plot(line_x, y, color=color, linestyle=style, linewidth=2.7,
                     label=rf"$\varphi={angle}^\circ$, $b=0$")
    axes[0].set_title("Gewichte drehen die Gerade")
    axes[0].legend(frameon=False, loc="upper left")
    phi = np.deg2rad(135)
    for bias, color, style in [(0, "#1D1D1F", "--"), (-0.75, "#C50018", "-")]:
        y = -(np.cos(phi) * line_x + bias) / np.sin(phi)
        axes[1].plot(line_x, y, color=color, linestyle=style, linewidth=2.7,
                     label=rf"$b={str(bias).replace('.', ',')}$")
    axes[1].set_title(r"Bias verschiebt bei gleichem $w$")
    axes[1].legend(frameon=False, loc="upper left")
    save_figure(fig, "boundary")
    plt.close(fig)

    values = np.linspace(0.5, 3.0, 300)
    loss = (2 * values - 4) ** 2
    fig, ax = plt.subplots(figsize=(10.6, 5.1), layout="constrained")
    ax.plot(values, loss, color="#1D1D1F", linewidth=2.7, label=r"$L(w)=(2w-4)^2$")
    ax.scatter([1, 1.8], [4, 0.16], c=["#1D1D1F", "#C50018"], s=95, zorder=5)
    ax.annotate("", xy=(1.8, 0.16), xytext=(1.02, 3.85),
                arrowprops={"arrowstyle": "->", "color": "#C50018", "linewidth": 2.5})
    ax.annotate(r"$w=1$, $L=4$", (1, 4), xytext=(0.58, 5.15), fontsize=18)
    ax.annotate(r"$w=1{,}8$, $L=0{,}16$", (1.8, 0.16), xytext=(1.83, 1.7), fontsize=18,
                color="#C50018")
    ax.set_xlabel(r"Gewicht $w$")
    ax.set_ylabel(r"Verlust $L(w)$")
    ax.set_ylim(-0.35, 9.4)
    ax.grid(alpha=0.5)
    ax.legend(frameon=False, loc="upper right")
    save_figure(fig, "gradient")
    plt.close(fig)

    fig, axes = plt.subplots(1, 2, figsize=(11.8, 4.9), layout="constrained")
    values = np.linspace(-2, 2, 300)
    axes[0].plot(values, np.maximum(0, values), color="#C50018", linewidth=3)
    axes[0].set_xlabel(r"Voraktivierung $z$")
    axes[0].set_ylabel(r"$\operatorname{ReLU}(z)$")
    axes[0].grid(alpha=0.5)
    diamond = np.array([[0, 1], [1, 0], [0, -1], [-1, 0], [0, 1]])
    axes[1].fill(diamond[:, 0], diamond[:, 1], color="#F5F5F7")
    axes[1].plot(diamond[:, 0], diamond[:, 1], color="#C50018", linewidth=3)
    axes[1].set_xlim(-1.55, 1.55)
    axes[1].set_ylim(-1.4, 1.4)
    axes[1].set_aspect("equal")
    axes[1].set_xlabel(r"Merkmal $x_1$")
    axes[1].set_ylabel(r"Merkmal $x_2$")
    axes[1].set_title(r"Beispielgrenze: $|x_1|+|x_2|=1$")
    axes[1].text(0, 0, "innen", ha="center", va="center", fontsize=18)
    axes[1].text(1.02, 1.12, "außen", ha="center", fontsize=18)
    axes[1].grid(alpha=0.4)
    save_figure(fig, "relu_regions")
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(10.6, 4.9), layout="constrained")
    ax.plot([row["epoch"] for row in history], [row["train_loss"] for row in history],
            color="#1D1D1F", linewidth=2.5, label="Training: Personen 1–16")
    ax.plot([row["epoch"] for row in history], [row["validation_loss"] for row in history],
            color="#C50018", linestyle="--", linewidth=2.5, label="Validierung: Personen 17–20")
    ax.set_xlabel("Epoche")
    ax.set_ylabel("Mittlerer Kreuzentropieverlust")
    ax.legend(frameon=False)
    ax.grid(alpha=0.5)
    save_figure(fig, "training")
    plt.close(fig)
    return features, feature_mean, feature_std


def main():
    windows, labels, subjects, local_windows, raw = load_windows()
    flat = windows.reshape(len(windows), 96)
    masks = {"train": subjects <= 16, "validation": (subjects >= 17) & (subjects <= 20),
             "test": subjects >= 21}
    assert [int(mask.sum()) for mask in masks.values()] == [768, 192, 192]
    parameters, mean, std, normalized, metrics, history = train_model(flat, labels, masks)
    assert sum(p.size for p in parameters) == 1603
    example_row = np.flatnonzero((subjects == 21) & (labels == 1) & (local_windows == 0))[0]
    scores = logits(normalized[[example_row]], parameters)[0]
    predicted = int(scores.argmax())
    model = {
        "purpose": "Reproducible classroom demo; no embedded timing or deployment validation",
        "architecture": [96, 16, 3], "hidden_activation": "ReLU", "output": "three unnormalized scores",
        "class_order": list(CLASSES), "input_layout": "32 samples, each x/y/z; flattened sample-major",
        "sample_rate_hz": SAMPLE_HZ, "window_samples": WINDOW, "window_duration_s": WINDOW / SAMPLE_HZ,
        "source_units": "g; raw acceleration including gravity", "dtype": "Float32",
        "normalization": {"mean": mean.tolist(), "std": std.tolist(), "fitted_subjects": list(range(1, 17))},
        "W1": parameters[0].tolist(), "b1": parameters[1].tolist(),
        "W2": parameters[2].tolist(), "b2": parameters[3].tolist(),
    }
    save_json("model-activity.json", model)
    summary = {
        "data_sha256": hashlib.sha256((DATA / "motionsense-activities.csv").read_bytes()).hexdigest(),
        "versions": {"python": platform.python_version(), "numpy": np.__version__},
        "training": {"seed": SEED, "epochs_fixed_in_advance": EPOCHS, "batch_size": BATCH_SIZE,
                     "optimizer": "Adam", "learning_rate": LEARNING_RATE,
                     "checkpoint_selection": "last fixed epoch, not selected by validation or test"},
        "network_parameter_count": 1603, "float32_network_bytes": 1603 * 4,
        "normalizer_values": 192, "float32_normalizer_bytes": 192 * 4,
        "window_counts": {name: int(mask.sum()) for name, mask in masks.items()},
        "subjects": {"train": list(range(1, 17)), "validation": list(range(17, 21)), "test": list(range(21, 25))},
        "metrics_exported_float32_model": metrics,
        "example": {"subject": 21, "activity_true": "walking", "local_window": 0,
                    "scores_in_class_order": [float(v) for v in scores],
                    "argmax": predicted, "activity_predicted": CLASSES[predicted]},
        "gradient_toy": {"L": "(2*w-4)^2", "w_before": 1, "eta": 0.1,
                         "derivative_before": -8, "w_after": 1.8, "L_before": 4, "L_after": 0.16},
        "history_every_10_epochs": history,
    }
    save_json("model-summary.json", summary)
    # Print the actual model result before plotting so authors can continue in parallel.
    print(json.dumps({"metrics": metrics, "example": summary["example"]}, ensure_ascii=False, indent=2), flush=True)
    features, feature_mean, feature_std = make_figures(windows, labels, subjects, raw, history)
    import matplotlib
    summary["versions"]["matplotlib"] = matplotlib.__version__
    summary["feature_view"] = {
        "description": "Two explanatory features; not the 96-entry network input",
        "mean_std_fitted_train_only": feature_mean.tolist(), "scale_std_fitted_train_only": feature_std.tolist(),
        "ranges_by_class": {activity: {"mean_g": [float(v) for v in (features[labels == k, 0].min(), features[labels == k, 0].max())],
                                            "std_g": [float(v) for v in (features[labels == k, 1].min(), features[labels == k, 1].max())]}
                            for k, activity in enumerate(CLASSES)},
    }
    save_json("model-summary.json", summary)
    print(f"Saved model and six SVG/PNG figure pairs under {FIGURES.relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    main()
