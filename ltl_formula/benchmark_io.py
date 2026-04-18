"""
Parse benchmark.txt: header A B, then A global LTL lines, then B lines of form 'i φ'.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class BenchmarkSpec:
    """Tasks from benchmark file (strings only; use parse_ltl for AST)."""

    global_formulas: tuple[str, ...]
    state_formulas: tuple[tuple[int, str], ...]


_STATE_LINE = re.compile(r"^\s*(\d+)\s+(.*)$")


def parse_benchmark_text(text: str) -> BenchmarkSpec:
    lines = text.splitlines()
    if not lines:
        raise ValueError("empty benchmark file")
    head = lines[0].split()
    if len(head) != 2:
        raise ValueError(f"line 1 must be 'A B', got: {lines[0]!r}")
    a, b = int(head[0]), int(head[1])
    rest = lines[1:]
    if len(rest) < a + b:
        raise ValueError(f"need {a + b} formula lines after header, got {len(rest)}")

    global_lines = tuple(s.strip() for s in rest[:a])
    state_block = rest[a : a + b]
    state_formulas: list[tuple[int, str]] = []
    for ln in state_block:
        m = _STATE_LINE.match(ln)
        if not m:
            raise ValueError(f"state formula line must be 'i φ', got: {ln!r}")
        sid = int(m.group(1))
        phi = m.group(2).strip()
        if not phi:
            raise ValueError(f"missing formula after state id: {ln!r}")
        state_formulas.append((sid, phi))

    return BenchmarkSpec(global_formulas=global_lines, state_formulas=tuple(state_formulas))


def load_benchmark_file(path: str | Path) -> BenchmarkSpec:
    return parse_benchmark_text(Path(path).read_text(encoding="utf-8"))
