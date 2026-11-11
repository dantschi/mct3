"""Setup behavior with local tool doubles; no downloads or real TeX required."""

import json
import os
from pathlib import Path
import platform
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
EXTRA_FILES = (
    "luatexbase.sty", "ctablestack.sty", "ngerman.ldf", "selnolig.sty",
    "loadhyph-de-1996.tex",
)
BASE_FILES = (
    "tcolorbox.sty", "sectsty.sty", "needspace.sty", "adjustbox.sty",
    "texgyreheros-regular.otf",
)

TOOL_DOUBLE = r'''import json
import os
from pathlib import Path
import sys

tool, args = sys.argv[1], sys.argv[2:]
with Path(os.environ["SETUP_TEST_EVENTS"]).open("a") as stream:
    stream.write(json.dumps({"tool": tool, "args": args}) + "\n")

if tool in ("curl", "wget", "unexpected-tex", "dpkg-deb"):
    print("Unexpected external operation: " + tool, file=sys.stderr)
    raise SystemExit(99)

files = Path(os.environ["SETUP_TEST_FILES"])
if tool == "kpsewhich":
    candidate = files / args[-1]
    if candidate.is_file():
        print(candidate)
        raise SystemExit(0)
    raise SystemExit(1)

if tool == "tlmgr":
    result = int(os.environ.get("SETUP_TEST_INSTALL_EXIT", "0"))
    if result:
        print("Deliberate package installation failure", file=sys.stderr)
        raise SystemExit(result)
    if os.environ.get("SETUP_TEST_INSTALL_NOOP") != "1":
        for name in json.loads(os.environ["SETUP_TEST_EXTRA_FILES"]):
            (files / name).write_text("installed fixture\n")
    raise SystemExit(0)

if tool == "lualatex" and args != ["--version"]:
    print("German LuaLaTeX smoke fixture")
    result = int(os.environ.get("SETUP_TEST_COMPILE_EXIT", "0"))
    if result:
        print("Deliberate German Babel compilation failure", file=sys.stderr)
        raise SystemExit(result)
    output = next(a.split("=", 1)[1] for a in args if a.startswith("-output-directory="))
    mode = os.environ.get("SETUP_TEST_PDF", "present")
    if mode != "missing":
        (Path(output) / "tex-smoke.pdf").write_bytes(
            b"" if mode == "empty" else b"%PDF-1.4\nfixture\n"
        )
    raise SystemExit(0)

print(tool + " fixture version")
'''


@unittest.skipUnless(
    platform.system() == "Linux" and platform.machine() == "x86_64",
    "The pinned toolchain supports Linux x86_64.",
)
class SetupTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="setup-test-")
        self.addCleanup(temporary.cleanup)
        self.workspace = Path(temporary.name)
        self.root = self.workspace / "repo"
        scripts = self.root / "scripts"
        scripts.mkdir(parents=True)
        for name in ("setup.sh", "setup-tex.sh", "activate.sh", "toolchain.env", "tex-smoke.tex"):
            shutil.copyfile(ROOT / "scripts" / name, scripts / name)

        # Read the real shell configuration without duplicating version pins.
        keys = (
            "QUARTO_VERSION", "QUARTO_SHA256", "NODE_VERSION", "NODE_SHA256",
            "TEXLIVE_VERSION", "TEXLIVE_SHA256", "CHROME_VERSION", "CHROME_SHA256",
            "RSVG_VERSION", "RSVG_SHA256", "TEXLIVE_REPOSITORY",
        )
        command = 'source "$1"; printf \'%s\\0\' ' + " ".join(
            '"${' + key + '}"' for key in keys
        ) + ' "${TEXLIVE_EXTRA_PACKAGES[@]}"'
        config = subprocess.run(
            ["bash", "-c", command, "setup-test", str(scripts / "toolchain.env")],
            capture_output=True, check=True,
        ).stdout.decode().split("\0")[:-1]
        self.config = dict(zip(keys, config[:len(keys)]))
        self.packages = config[len(keys):]

        self.toolchain = self.workspace / "tools"
        self.files = self.workspace / "tex-files"
        self.files.mkdir()
        self.events = self.workspace / "events.jsonl"
        self.driver = self.workspace / "tool_double.py"
        self.driver.write_text(TOOL_DOUBLE, encoding="utf-8")
        shims = self.workspace / "shims"
        shims.mkdir()
        for name in ("curl", "wget", "dpkg-deb"):
            self.executable(shims / name, name)
        # A fallback to a system TeX installation must not hide a broken fixture.
        for name in ("lualatex", "kpsewhich", "tlmgr"):
            self.executable(shims / name, "unexpected-tex")

        self.env = os.environ.copy()
        self.env.update({
            "DHBW_TOOLCHAIN_DIR": str(self.toolchain),
            "PATH": str(shims) + os.pathsep + os.defpath,
            "SETUP_TEST_EVENTS": str(self.events),
            "SETUP_TEST_FILES": str(self.files),
            "SETUP_TEST_EXTRA_FILES": json.dumps(EXTRA_FILES),
        })

    def executable(self, path, tool):
        path.parent.mkdir(parents=True, exist_ok=True)
        command = " ".join(map(shlex.quote, (sys.executable, str(self.driver), tool)))
        path.write_text('#!/bin/sh\nexec ' + command + ' "$@"\n', encoding="utf-8")
        path.chmod(0o755)

    def provision(self, full=True, extras=True):
        components = ("QUARTO", "NODE", "TEXLIVE", "CHROME", "RSVG") if full else ("QUARTO",)
        prefixes = {"TEXLIVE": "texlive", "CHROME": "chrome", "RSVG": "rsvg"}
        paths = {}
        for component in components:
            prefix = prefixes.get(component, component.lower())
            directory = self.toolchain / (prefix + "-" + self.config[component + "_VERSION"])
            directory.mkdir(parents=True)
            (directory / ".installed-sha256").write_text(self.config[component + "_SHA256"] + "\n")
            paths[component] = directory
        self.executable(paths["QUARTO"] / "bin/quarto", "quarto")
        if not full:
            return
        self.executable(paths["NODE"] / "bin/node", "node")
        self.executable(paths["CHROME"] / "chrome-headless-shell-linux64/chrome-headless-shell", "chrome")
        self.executable(paths["RSVG"] / "usr/bin/rsvg-convert", "rsvg-convert")
        for name in ("kpsewhich", "tlmgr", "lualatex"):
            self.executable(paths["TEXLIVE"] / "bin/x86_64-linux" / name, name)
        for name in BASE_FILES + (EXTRA_FILES if extras else ()):
            (self.files / name).write_text("fixture\n")

    def run_setup(self, *arguments, helper=False, **overrides):
        script = "setup-tex.sh" if helper else "setup.sh"
        return subprocess.run(
            ["bash", str(self.root / "scripts" / script), *arguments],
            cwd=self.root, env={**self.env, **overrides},
            capture_output=True, text=True, timeout=20,
        )

    def calls(self, tool):
        if not self.events.exists():
            return []
        return [
            event["args"] for line in self.events.read_text().splitlines()
            if (event := json.loads(line))["tool"] == tool
        ]

    def compile_calls(self):
        return [args for args in self.calls("lualatex") if args != ["--version"]]

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_quarto_only_does_not_require_tex(self):
        self.provision(full=False)
        self.assert_success(self.run_setup("--quarto-only"))
        self.assertEqual(self.calls("quarto"), [["--version"]])
        self.assertFalse(self.calls("unexpected-tex"))
        self.assertFalse(self.calls("curl"))
        self.assertFalse((self.toolchain / "checks").exists())

    def test_full_setup_repairs_missing_packages_from_configured_repository(self):
        self.provision(extras=False)
        self.assert_success(self.run_setup())
        self.assertEqual(self.calls("tlmgr"), [[
            "--verify-repo=all", "--repository", self.config["TEXLIVE_REPOSITORY"],
            "install", *self.packages,
        ]])
        self.assertTrue(all((self.files / name).is_file() for name in EXTRA_FILES))
        self.assertEqual(len(self.compile_calls()), 1)
        self.assertEqual(Path(self.compile_calls()[0][-1]), self.root / "scripts/tex-smoke.tex")
        self.assertIn("German LuaLaTeX smoke fixture", (self.toolchain / "checks/tex-smoke.log").read_text())
        self.assertFalse(self.calls("curl"))

    def test_package_installation_failure_stops_full_setup(self):
        self.provision(extras=False)
        result = self.run_setup(SETUP_TEST_INSTALL_EXIT="37")
        self.assertEqual(result.returncode, 37, result.stdout + result.stderr)
        self.assertIn("Deliberate package installation failure", result.stderr)
        self.assertFalse(self.compile_calls())

    def test_existing_babel_does_not_hide_missing_german_language_dependencies(self):
        self.provision()
        for count, name in enumerate(("ngerman.ldf", "loadhyph-de-1996.tex"), 1):
            with self.subTest(missing=name):
                (self.files / name).unlink()
                self.assert_success(self.run_setup(helper=True))
                self.assertEqual(len(self.calls("tlmgr")), count)
                self.assertTrue((self.files / name).is_file())
                self.assertEqual(len(self.compile_calls()), count)

    def test_installer_success_does_not_hide_still_missing_files(self):
        self.provision(extras=False)
        result = self.run_setup(helper=True, SETUP_TEST_INSTALL_NOOP="1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Required TeX file is missing after setup: luatexbase.sty", result.stderr)
        self.assertFalse(self.compile_calls())

    def test_file_presence_does_not_hide_german_compilation_failure(self):
        self.provision()
        result = self.run_setup(SETUP_TEST_COMPILE_EXIT="42")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(self.calls("tlmgr"))
        self.assertIn("German LuaLaTeX check failed", result.stderr)
        log = self.toolchain / "checks/tex-smoke.log"
        self.assertIn("Deliberate German Babel compilation failure", log.read_text())
        self.assertFalse(list(self.toolchain.glob(".tex-check.*")))

    def test_compiler_success_requires_a_nonempty_fresh_pdf(self):
        self.provision()
        checks = self.toolchain / "checks"
        checks.mkdir()
        (checks / "tex-smoke.pdf").write_bytes(b"%PDF-old-success\n")
        for mode in ("missing", "empty"):
            with self.subTest(mode=mode):
                result = self.run_setup(helper=True, SETUP_TEST_PDF=mode)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn("German LuaLaTeX check produced no PDF", result.stderr)
                self.assertFalse(list(self.toolchain.glob(".tex-check.*")))

    def test_repeated_full_setup_reuses_packages_but_checks_tex_again(self):
        self.provision(extras=False)
        self.assert_success(self.run_setup())
        self.assert_success(self.run_setup())
        self.assertEqual(len(self.calls("tlmgr")), 1)
        calls = self.compile_calls()
        self.assertEqual(len(calls), 2)
        output = lambda args: next(a for a in args if a.startswith("-output-directory="))
        self.assertNotEqual(output(calls[0]), output(calls[1]))
        self.assertFalse(list(self.toolchain.glob(".tex-check.*")))
        self.assertFalse(self.calls("curl"))


if __name__ == "__main__":
    unittest.main()
