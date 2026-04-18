#!/usr/bin/env python3
"""
Build (CMake) and run LTL-verifier, run Python src/main.py on the same TS + benchmark,
and print a line-by-line diff of the A+B output bits.

All file arguments are interpreted relative to the repository root unless absolute.

Usage (from repo root):
  python3 tools/compare_ltl_verifier.py [TS.txt] [benchmark.txt]

Requires: g++, CMake 3.20+, network once for ANTLR fetch (or populate build/_deps manually).

Python deps: from repo root run `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
(PEP 668 systems cannot `pip install` into the system interpreter). Set LTL_PYTHON to override.
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_VERIFIER_SUBDIR = Path("LTL-verifier")
_PY_MAIN_REL = Path("src") / "main.py"
_DEFAULT_CMAKE = Path.home() / ".local" / "cmake" / "bin" / "cmake"


def _find_repo_python() -> str:
    env = os.environ.get("LTL_PYTHON", "").strip()
    if env:
        return env
    for name in ("python3", "python"):
        cand = _ROOT / ".venv" / "bin" / name
        if cand.is_file():
            return str(cand)
    return sys.executable


def _find_cmake() -> str:
    env = os.environ.get("CMAKE", "").strip()
    if env:
        return env
    if _DEFAULT_CMAKE.is_file():
        return str(_DEFAULT_CMAKE)
    c = shutil.which("cmake")
    if c:
        return c
    sys.stderr.write(
        "cmake not found. Install CMake or set CMAKE to the binary "
        f"(e.g. {_DEFAULT_CMAKE}).\n"
    )
    sys.exit(2)
    raise SystemExit  # unreachable


def _repo_resolve(p: Path) -> Path:
    """Path relative to repo root, or absolute path as given."""
    if p.is_absolute():
        return p
    return (_ROOT / p).resolve()


def _repo_relpath(p: Path) -> str:
    """Path as string relative to repo root when possible (for subprocess argv)."""
    p = p.resolve()
    try:
        return os.path.relpath(p, _ROOT)
    except ValueError:
        return str(p)


def _build_verifier(build_dir: Path, cmake: str) -> Path:
    build_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            cmake,
            "-S",
            _repo_relpath(_ROOT / _VERIFIER_SUBDIR),
            "-B",
            _repo_relpath(build_dir),
            "-DCMAKE_BUILD_TYPE=Release",
        ],
        cwd=_ROOT,
        check=True,
    )
    subprocess.run([cmake, "--build", _repo_relpath(build_dir), "-j"], cwd=_ROOT, check=True)
    exe = build_dir / "LTL-verifier"
    if not exe.is_file():
        exe = build_dir / "Release" / "LTL-verifier"
    if not exe.is_file():
        raise FileNotFoundError(f"built binary not found under {build_dir}")
    return exe


def _run_capture(argv: list[str], cwd: Path) -> str:
    r = subprocess.run(
        argv,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        check=False,
    )
    if r.returncode != 0:
        sys.stderr.write(f"command failed ({r.returncode}): {argv!r}\n")
        sys.stderr.write(r.stderr)
        sys.stderr.write(r.stdout)
        sys.exit(r.returncode)
    return r.stdout


def main() -> None:
    ap = argparse.ArgumentParser(description="Diff Python LTL checker vs LTL-verifier.")
    ap.add_argument(
        "ts",
        type=Path,
        nargs="?",
        default=Path("project_benchmark") / "TS.txt",
        help="TS file (default: project_benchmark/TS.txt, relative to repo root)",
    )
    ap.add_argument(
        "benchmark",
        type=Path,
        nargs="?",
        default=Path("project_benchmark") / "benchmark1.txt",
        help="benchmark file (default: project_benchmark/benchmark1.txt)",
    )
    ap.add_argument(
        "--build-dir",
        type=Path,
        default=_VERIFIER_SUBDIR / "build-cmake",
        help="CMake build dir (default: LTL-verifier/build-cmake)",
    )
    ap.add_argument("--no-build", action="store_true", help="Skip CMake; use existing binary in build-dir")
    args = ap.parse_args()

    ts = _repo_resolve(args.ts)
    bench = _repo_resolve(args.benchmark)
    build_dir = _repo_resolve(args.build_dir)
    if not ts.is_file() or not bench.is_file():
        sys.stderr.write("TS or benchmark file not found.\n")
        sys.exit(1)

    cmake = _find_cmake()
    if args.no_build:
        exe = build_dir / "LTL-verifier"
        if not exe.is_file():
            sys.stderr.write(f"--no-build but missing {exe}\n")
            sys.exit(1)
    else:
        exe = _build_verifier(build_dir, cmake)

    out_cpp = build_dir / "result_compare.txt"
    subprocess.run(
        [
            _repo_relpath(exe),
            _repo_relpath(ts),
            _repo_relpath(bench),
            _repo_relpath(out_cpp),
        ],
        cwd=_ROOT,
        check=True,
    )
    cpp_lines = out_cpp.read_text(encoding="utf-8").splitlines()

    py_exe = _find_repo_python()
    py_out = _run_capture(
        [py_exe, _repo_relpath(_ROOT / _PY_MAIN_REL), _repo_relpath(ts), _repo_relpath(bench)],
        _ROOT,
    )
    py_lines = py_out.splitlines()

    n = max(len(cpp_lines), len(py_lines))
    mismatches = 0
    print(f"TS={_repo_relpath(ts)}\nbenchmark={_repo_relpath(bench)}\nindex cpp  py  ok")
    for i in range(n):
        a = cpp_lines[i] if i < len(cpp_lines) else "<missing>"
        b = py_lines[i] if i < len(py_lines) else "<missing>"
        ok = "yes" if a == b else "NO"
        if a != b:
            mismatches += 1
        print(f"{i:5}  {a:>4} {b:>4}  {ok}")

    print(f"\nTotal lines: cpp={len(cpp_lines)} py={len(py_lines)} mismatches={mismatches}")
    if mismatches:
        sys.exit(1)


if __name__ == "__main__":
    main()
