#!/usr/bin/env python3
"""Reproduce the small VL08 selection from the pinned MotionSense archive.

The downloaded archive stays outside the repository. Measurements are selected,
not normalized, resampled, interpolated or synthesized.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import urllib.request
import zipfile


UPSTREAM_COMMIT = "261cb0d60611a049ab38127738e42cc510ed50f4"
ARCHIVE_SHA256 = "0bf7446dd2e6aca6f7a6ea55012c7e3d7a43887c34c6d05d480473f3216ee07b"
ARCHIVE_URL = (
    "https://raw.githubusercontent.com/mmalekzadeh/motion-sense/"
    f"{UPSTREAM_COMMIT}/data/B_Accelerometer_data.zip"
)
ACTIVITIES = {"standing": "std_6", "walking": "wlk_7", "jogging": "jog_9"}
SAMPLES = 512


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    if not args.archive.exists():
        args.archive.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(ARCHIVE_URL, timeout=60) as response:
            args.archive.write_bytes(response.read())
    archive_data = args.archive.read_bytes()
    archive_sha = hashlib.sha256(archive_data).hexdigest()
    if archive_sha != ARCHIVE_SHA256:
        raise ValueError(f"Unexpected archive SHA-256: {archive_sha}")
    args.output.mkdir(parents=True, exist_ok=True)
    csv_path = args.output / "motionsense-activities.csv"
    selections = []
    with zipfile.ZipFile(io.BytesIO(archive_data)) as archive:
        with csv_path.open("w", encoding="utf-8", newline="") as target:
            writer = csv.writer(target, lineterminator="\n")
            writer.writerow(["subject", "activity", "trial", "sample", "x", "y", "z"])
            for subject in range(1, 25):
                for activity, trial in ACTIVITIES.items():
                    name = f"B_Accelerometer_data/{trial}/sub_{subject}.csv"
                    raw = archive.read(name)
                    records = list(csv.DictReader(io.StringIO(raw.decode("utf-8"))))
                    if len(records) < SAMPLES:
                        raise ValueError(f"Too few samples: {name}")
                    start = (len(records) - SAMPLES) // 2
                    selected = records[start : start + SAMPLES]
                    indices = [int(row[""]) for row in selected]
                    if indices != list(range(indices[0], indices[0] + SAMPLES)):
                        raise ValueError(f"Non-contiguous original sample indices: {name}")
                    for row in selected:
                        if not all(math.isfinite(float(row[axis])) for axis in "xyz"):
                            raise ValueError(f"Non-finite measurement: {name}")
                        writer.writerow(
                            [subject, activity, trial, row[""], row["x"], row["y"], row["z"]]
                        )
                    selections.append(
                        {
                            "subject": subject,
                            "activity": activity,
                            "trial": trial,
                            "archive_member": name,
                            "archive_member_sha256": hashlib.sha256(raw).hexdigest(),
                            "original_samples": len(records),
                            "first_sample": indices[0],
                            "last_sample": indices[-1],
                        }
                    )
    provenance = {
        "dataset": "MotionSense, Accelerometer data (B)",
        "authors": "Mohammad Malekzadeh, Richard G. Clegg, Andrea Cavallaro, Hamed Haddadi",
        "upstream_repository": "https://github.com/mmalekzadeh/motion-sense",
        "upstream_commit": UPSTREAM_COMMIT,
        "archive_url": ARCHIVE_URL,
        "archive_sha256": archive_sha,
        "license": "MIT",
        "license_copyright": "Copyright (c) 2018 Mohammad Malekzadeh",
        "license_url": (
            "https://github.com/mmalekzadeh/motion-sense/blob/"
            f"{UPSTREAM_COMMIT}/LICENSE"
        ),
        "paper_doi": "10.1145/3302505.3310068",
        "sample_rate_hz": 50,
        "acceleration_unit": "g (Core Motion CMAcceleration, including gravity)",
        "window_samples": 32,
        "window_overlap_samples": 0,
        "samples_per_subject_activity": SAMPLES,
        "subjects": 24,
        "records": len(selections),
        "csv_rows": len(selections) * SAMPLES,
        "windows": len(selections) * SAMPLES // 32,
        "selection": "Central 512 consecutive samples of the selected original trial; unchanged x/y/z strings.",
        "splits": {"train": list(range(1, 17)), "validation": list(range(17, 21)), "test": list(range(21, 25))},
        "csv_sha256": hashlib.sha256(csv_path.read_bytes()).hexdigest(),
        "selections": selections,
    }
    (args.output / "provenance.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{csv_path}: {provenance['csv_rows']} measurements, {provenance['windows']} windows")
    print(f"Archive SHA-256: {archive_sha}")
    print(f"CSV SHA-256: {provenance['csv_sha256']}")


if __name__ == "__main__":
    main()
