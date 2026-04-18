"""LTL model checking by searching counterexamples in TS × A_{¬φ}."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable, Sequence
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
# Default input files under repository root.
_DEFAULT_TS_REL = Path("project_benchmark") / "TS.txt"
_DEFAULT_BENCHMARK_REL = Path("project_benchmark") / "benchmark1.txt"
DEFAULT_TS_PATH = _ROOT / _DEFAULT_TS_REL
DEFAULT_BENCHMARK_PATH = _ROOT / _DEFAULT_BENCHMARK_REL
_SRC = Path(__file__).resolve().parent
for _p in (_ROOT, _SRC):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import ltl_formula.ast as ast
from GNBA import GNBA, NBA, prune_nba_unreachable
from ltl_formula import (
    TransitionSystem,
    intern_formula,
    load_benchmark_file,
    load_ts_file,
    parse_ltl,
)


def ts_label_as_names(ts: TransitionSystem, state: int) -> frozenset[str]:
    return frozenset(ts.ap_names[i] for i in ts.labels[state])


def label_matches_elementary(
    ts_names: frozenset[str], elem_ap: frozenset[str], ap_alphabet: frozenset[str]
) -> bool:
    """For every AP that occurs in the formula, truth value in TS must match the elementary set."""
    for a in ap_alphabet:
        if (a in ts_names) != (a in elem_ap):
            return False
    return True


def forward_reachable(adj: Sequence[Sequence[int]], starts: Iterable[int]) -> frozenset[int]:
    seen: set[int] = set()
    stack = list(starts)
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        for v in adj[u]:
            stack.append(v)
    return frozenset(seen)


_WHITE, _CYAN, _BLUE = 0, 1, 2


def buchi_language_nonempty(adj: Sequence[Sequence[int]], initial: Iterable[int], accept: frozenset[int]) -> bool:
    """
    Büchi 语言非空：存在从初态可达的、含接受态的有向环（Nested DFS；教材 Algorithm 8 等价判据）。
    """
    reachable = forward_reachable(adj, initial)
    n = len(adj)
    color: list[int] = [_WHITE] * n

    def dfs2(v: int, red: set[int]) -> bool:
        red.add(v)
        for w in adj[v]:
            if w not in reachable:
                continue
            if color[w] == _CYAN:
                return True
            if color[w] != _BLUE and w not in red and dfs2(w, red):
                return True
        return False

    def dfs1(v: int) -> bool:
        color[v] = _CYAN
        for w in adj[v]:
            if w not in reachable:
                continue
            if color[w] == _WHITE and dfs1(w):
                return True
        if v in accept and dfs2(v, set()):
            return True
        color[v] = _BLUE
        return False

    for s0 in initial:
        if s0 in reachable and color[s0] == _WHITE and dfs1(s0):
            return True
    return False


def verifier_find_loop(
    ts: TransitionSystem,
    nba: NBA,
    elem_labels: Sequence[frozenset[str]],
    ap_alphabet: frozenset[str],
    start_state: int,
) -> bool:
    """
    同 LTL-verifier `loop.cpp` / `FindLoop`：在 TS 与（已 NBA 化的）自动机上找
    「栈上闭合路径且路径段上接受态计数增加」的 witness。返回 True 表示存在反例路径起点模式。
    """

    def get_next_states(q: int, t_label: frozenset[str]) -> list[int]:
        g = nba.gnba_state_for_nba_state[q]
        if not label_matches_elementary(t_label, elem_labels[g], ap_alphabet):
            return []
        return list(nba.edges[q])

    def is_final(q: int) -> bool:
        return q in nba.accept

    def run_from_root(root_q: int) -> bool:
        stack: list[tuple[int, int]] = []
        record_final: dict[tuple[int, int], int] = {}
        visited: set[tuple[int, int]] = set()
        num_final = 0

        def dfs(s: int, q: int) -> bool:
            nonlocal num_final
            pair = (s, q)
            if pair in stack:
                return record_final[pair] < num_final
            if pair in visited:
                return False
            visited.add(pair)
            stack.append(pair)
            record_final[pair] = num_final
            num_final += 1 if is_final(q) else 0
            try:
                for _act, t in _ts_successors(ts, s):
                    t_label = ts_label_as_names(ts, t)
                    for p in get_next_states(q, t_label):
                        if dfs(t, p):
                            return True
                return False
            finally:
                num_final -= 1 if is_final(q) else 0
                stack.pop()

        return dfs(start_state, root_q)

    names0 = ts_label_as_names(ts, start_state)
    seen_q: set[int] = set()
    for q0 in nba.initial_states:
        for q in get_next_states(q0, names0):
            if q in seen_q:
                continue
            seen_q.add(q)
            # Do not share visited across roots; it can hide valid cycles.
            if run_from_root(q):
                return True
    return False


def counterexample_exists_verifier(
    ts: TransitionSystem,
    nba: NBA,
    elem_labels: Sequence[frozenset[str]],
    ap_alphabet: frozenset[str],
    start_states: frozenset[int],
) -> bool:
    """存在从某个 s ∈ start_states 出发的、verifier_find_loop 能捕获的反例。"""
    return any(verifier_find_loop(ts, nba, elem_labels, ap_alphabet, s0) for s0 in start_states)


def build_ts_nba_product(
    ts: TransitionSystem,
    nba: NBA,
    ap_alphabet: frozenset[str],
    elem_labels: Sequence[frozenset[str]],
) -> tuple[int, list[list[int]], list[int], frozenset[int]]:
    """
    Product Büchi automaton for TS × A: states are (s, q) flattened as s * nba.n_states + q.

    Matches LTL-verifier `FindLoop` / `loop.cpp`: from (s, q), for each TS edge s→t, the NBA reads **L(t)**
    and may move q→q' only if that letter matches **source** state q's elementary AP label (GNBA transition key).
    Initial pairs are (s0, q') where q' is a successor of some NBA initial q0 on reading L(s0).
    """
    n_ts, n_q = ts.num_states, nba.n_states
    prod_n = n_ts * n_q
    adj: list[list[int]] = [[] for _ in range(prod_n)]

    def enc(s: int, q: int) -> int:
        return s * n_q + q

    for s in range(n_ts):
        for q in range(n_q):
            g = nba.gnba_state_for_nba_state[q]
            for _act, s2 in _ts_successors(ts, s):
                t_names = ts_label_as_names(ts, s2)
                if not label_matches_elementary(t_names, elem_labels[g], ap_alphabet):
                    continue
                for q2 in nba.edges[q]:
                    adj[enc(s, q)].append(enc(s2, q2))

    for u in range(prod_n):
        adj[u] = sorted(set(adj[u]))

    initial: list[int] = []
    for s0 in ts.initial_states:
        names0 = ts_label_as_names(ts, s0)
        for q0 in nba.initial_states:
            g0 = nba.gnba_state_for_nba_state[q0]
            if not label_matches_elementary(names0, elem_labels[g0], ap_alphabet):
                continue
            for q2 in nba.edges[q0]:
                initial.append(enc(s0, q2))
    initial = sorted(set(initial))

    accept = frozenset(enc(s, q) for s in range(n_ts) for q in nba.accept if q < n_q)
    return prod_n, adj, initial, accept


def _ts_successors(ts: TransitionSystem, s: int) -> list[tuple[int, int]]:
    return [(k, j) for (i, k, j) in ts.transitions if i == s]


def build_ts_nba_product_from_starts(
    ts: TransitionSystem,
    nba: NBA,
    ap_alphabet: frozenset[str],
    elem_labels: Sequence[frozenset[str]],
    start_states: frozenset[int],
) -> tuple[list[list[int]], list[int], frozenset[int]]:
    """Same product as `build_ts_nba_product` but Büchi-emptiness starts from S0' ⊆ start_states × Q0."""
    _n, adj, _full_init, accept = build_ts_nba_product(ts, nba, ap_alphabet, elem_labels)
    n_q = nba.n_states
    initial = []
    for s0 in start_states:
        names0 = ts_label_as_names(ts, s0)
        for q0 in nba.initial_states:
            g0 = nba.gnba_state_for_nba_state[q0]
            if not label_matches_elementary(names0, elem_labels[g0], ap_alphabet):
                continue
            for q2 in nba.edges[q0]:
                initial.append(s0 * n_q + q2)
    initial = sorted(set(initial))
    return adj, initial, accept


def ts_satisfies_ltl(
    ts: TransitionSystem,
    phi: ast.Formula,
    start_states: frozenset[int],
) -> bool:
    """
    ∀ paths π starting from some s ∈ start_states, π |= φ
    iff no path yields a word in L(¬φ), tested via non-emptiness of TS × A_{¬φ}.
    """
    neg = intern_formula(ast.Not(phi))
    g = GNBA(neg)
    g.remove_unreachable()
    nba = g.to_nba()
    nba = prune_nba_unreachable(nba)
    has_counterexample = counterexample_exists_verifier(ts, nba, g.ap_labels, g.ap_alphabet, start_states)
    return not has_counterexample


def run_benchmark(ts_path: Path, bench_path: Path) -> list[int]:
    ts = load_ts_file(ts_path)
    spec = load_benchmark_file(bench_path)
    out: list[int] = []
    for fstr in spec.global_formulas:
        phi = parse_ltl(fstr)
        ok = ts_satisfies_ltl(ts, phi, ts.initial_states)
        out.append(1 if ok else 0)
    for sid, fstr in spec.state_formulas:
        phi = parse_ltl(fstr)
        ok = ts_satisfies_ltl(ts, phi, frozenset({sid}))
        out.append(1 if ok else 0)
    return out


def build_arg_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="LTL model checking: read TS.txt and benchmark.txt; print A+B lines of 1/0 per README.",
    )
    ap.add_argument(
        "ts",
        type=Path,
        nargs="?",
        default=DEFAULT_TS_PATH,
        help=f"path to TS.txt (default: {_DEFAULT_TS_REL})",
    )
    ap.add_argument(
        "benchmark",
        type=Path,
        nargs="?",
        default=DEFAULT_BENCHMARK_PATH,
        help=f"path to benchmark.txt (default: {_DEFAULT_BENCHMARK_REL})",
    )
    return ap


def parse_cli_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    return build_arg_parser().parse_args(argv)


def main(argv: Sequence[str] | None = None) -> None:
    args = parse_cli_args(argv)
    for r in run_benchmark(args.ts, args.benchmark):
        print(r)


if __name__ == "__main__":
    main()
