"""
Parse TS.txt into a transition system (Input_Format.pdf).

Layout: S T | initial states | A actions | P AP names | T transitions (i,k,j) | S label lines (-1 = empty).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import FrozenSet, Sequence, Tuple


@dataclass(frozen=True)
class TransitionSystem:
    """Finite transition system TS = (S, Act, AP, →, I, L)."""

    num_states: int  # S
    num_transitions: int  # T (redundant with len(transitions); kept for checks)
    initial_states: FrozenSet[int]
    actions: Tuple[int, ...]  # listed Act; |actions| = A
    ap_names: Tuple[str, ...]  # P names, indices 0 .. P-1
    transitions: Tuple[Tuple[int, int, int], ...]  # (source, action_index, target) = s_i -α_k-> s_j
    labels: Tuple[FrozenSet[int], ...]  # L(s_i) as AP indices, len == S

    @property
    def num_actions(self) -> int:
        return len(self.actions)

    @property
    def num_ap(self) -> int:
        return len(self.ap_names)


def parse_ts_text(text: str) -> TransitionSystem:
    """Parse full `TS.txt` content."""
    lines = [ln.strip() for ln in text.splitlines() if ln.strip() != ""]
    if len(lines) < 4:
        raise ValueError("TS file too short (need at least S T, I, Act, AP header lines)")

    s_t = lines[0].split()
    if len(s_t) != 2:
        raise ValueError(f"line 1 must be 'S T', got: {lines[0]!r}")
    s_count, t_count = int(s_t[0]), int(s_t[1])

    if s_count < 0 or t_count < 0:
        raise ValueError("S and T must be non-negative")

    initial_raw = lines[1].split()
    initial_states = frozenset(int(x) for x in initial_raw)
    for q in initial_states:
        if q < 0 or q >= s_count:
            raise ValueError(f"initial state {q} out of range [0, {s_count - 1}]")

    act_tokens = lines[2].split()
    if not act_tokens:
        raise ValueError("line 3 (actions Act) must not be empty")
    actions = tuple(int(x) for x in act_tokens)
    a_dim = len(actions)

    ap_line = lines[3].split()
    if not ap_line:
        raise ValueError("line 4 (atomic propositions) must not be empty")
    ap_names = tuple(ap_line)
    p_dim = len(ap_names)

    need = 4 + t_count + s_count
    if len(lines) < need:
        raise ValueError(
            f"expected {need} non-empty lines, got {len(lines)} (S={s_count}, T={t_count})"
        )

    trans_start = 4
    trans: list[tuple[int, int, int]] = []
    for ti in range(t_count):
        parts = lines[trans_start + ti].split()
        if len(parts) != 3:
            raise ValueError(f"transition line must be i k j, got: {lines[trans_start + ti]!r}")
        i, k, j = int(parts[0]), int(parts[1]), int(parts[2])
        if not (0 <= i < s_count and 0 <= j < s_count):
            raise ValueError(f"transition ({i},{k},{j}): states must be in [0, {s_count - 1}]")
        if not (0 <= k < a_dim):
            raise ValueError(
                f"transition ({i},{k},{j}): action index k must be in [0, {a_dim - 1}]"
            )
        trans.append((i, k, j))

    lab_start = trans_start + t_count
    labels_list: list[frozenset[int]] = []
    for si in range(s_count):
        raw = lines[lab_start + si]
        labels_list.append(_parse_label_line(raw, p_dim))

    return TransitionSystem(
        num_states=s_count,
        num_transitions=t_count,
        initial_states=initial_states,
        actions=actions,
        ap_names=ap_names,
        transitions=tuple(trans),
        labels=tuple(labels_list),
    )


def _parse_label_line(line: str, p_dim: int) -> FrozenSet[int]:
    parts = line.split()
    if len(parts) == 1 and parts[0] == "-1":
        return frozenset()
    out: set[int] = set()
    for t in parts:
        x = int(t)
        if x < 0 or x >= p_dim:
            raise ValueError(f"AP index {x} out of range [0, {p_dim - 1}] in label line: {line!r}")
        out.add(x)
    return frozenset(out)


def load_ts_file(path: str | Path) -> TransitionSystem:
    return parse_ts_text(Path(path).read_text(encoding="utf-8"))


def ap_index(ts: TransitionSystem, name: str) -> int:
    """Map atomic proposition symbol to index; raises ValueError if unknown."""
    try:
        return ts.ap_names.index(name)
    except ValueError as e:
        raise ValueError(f"AP {name!r} not in {ts.ap_names}") from e
