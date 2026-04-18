from __future__ import annotations

import itertools
from collections.abc import Iterable
from dataclasses import dataclass

import ltl_formula.ast as ast


def _forward_reachable(adj: list[list[int]], starts: Iterable[int]) -> frozenset[int]:
    seen: set[int] = set()
    stack = list(starts)
    while stack:
        u = stack.pop()
        if u in seen:
            continue
        seen.add(u)
        if u < len(adj):
            for v in adj[u]:
                stack.append(v)
    return frozenset(seen)


@dataclass(frozen=True)
class NBA:
    """
    Nondeterministic Büchi automaton (states are integers 0 .. n_states-1).
    `gnba_state_for_nba_state[i]` is the elementary-set index of the underlying GNBA state.
    """

    n_states: int
    edges: list[list[int]]
    initial_states: list[int]
    accept: frozenset[int]
    gnba_state_for_nba_state: tuple[int, ...]


def _ast_node_count(formula: ast.Formula) -> int:
    """Number of AST nodes (root included); larger means more structurally complex."""
    if isinstance(formula, ast.Prop):
        return 1
    if isinstance(formula, (ast.Not, ast.Next, ast.Finally, ast.Globally)):
        return 1 + _ast_node_count(formula.inner)
    if isinstance(formula, (ast.And, ast.Or, ast.Implies, ast.Until)):
        return 1 + _ast_node_count(formula.left) + _ast_node_count(formula.right)
    raise TypeError(type(formula))


def visit_formula(formula: ast.Formula) -> list[ast.Formula]:
    """
    Closure for GNBA elementary sets: syntactic subformulas of φ (including φ), plus
    for each Until / Finally / Globally subformula ψ the formula Xψ (analogous to
    LTL-verifier when `Next(ψ)` is a subformula; we adjoin Xψ in the same DFS so
    tableau rules need no separate expansion pass).

    Uniqueness is by AST value: frozen subformulas are deduped in a set (e.g. shared
    leaves such as the two `a` in `a /\\ a` appear once).

    Returned list is sorted simple → complex using AST node count, then `format_formula`
    for deterministic ties.
    """
    closure: set[ast.Formula] = set()

    def visit(f: ast.Formula) -> None:
        closure.add(f)
        if isinstance(f, ast.Prop):
            return
        if isinstance(f, (ast.Not, ast.Next)):
            visit(f.inner)
            return
        if isinstance(f, (ast.Finally, ast.Globally)):
            visit(f.inner)
            closure.add(ast.Next(f))
            return
        if isinstance(f, (ast.And, ast.Or, ast.Implies, ast.Until)):
            visit(f.left)
            visit(f.right)
            if isinstance(f, ast.Until):
                closure.add(ast.Next(f))
            return
        raise TypeError(type(f))

    visit(formula)
    return sorted(
        closure,
        key=lambda f: (_ast_node_count(f), ast.format_formula(f)),
    )


def _closure_sort_key(f: ast.Formula) -> tuple[int, str]:
    return (_ast_node_count(f), ast.format_formula(f))


def is_consistent(subset: set[ast.Formula], closure: set[ast.Formula]) -> bool:
    """
    Local (tableau) consistency of B ⊆ cl(φ): propositional / boolean / Until / F / G rules
    relative to the full closure from `visit_formula`. B must only contain formulas from closure.
    """
    if not subset.issubset(closure):
        return False

    for psi in closure:
        if isinstance(psi, ast.Not):
            inner = psi.inner
            if (psi in subset) != (inner not in subset):
                return False

    for f in closure:
        if isinstance(f, ast.And):
            l, r = f.left, f.right
            if (f in subset) != ((l in subset) and (r in subset)):
                return False
        elif isinstance(f, ast.Or):
            l, r = f.left, f.right
            if (f in subset) != ((l in subset) or (r in subset)):
                return False
        elif isinstance(f, ast.Implies):
            l, r = f.left, f.right
            if (f in subset) != ((l not in subset) or (r in subset)):
                return False
        elif isinstance(f, ast.Until):
            l, r = f.left, f.right
            xu = ast.Next(f)
            if xu not in closure:
                return False
            if (f in subset) != ((r in subset) or ((l in subset) and (xu in subset))):
                return False
        elif isinstance(f, ast.Finally):
            inner = f.inner
            xf = ast.Next(f)
            if xf not in closure:
                return False
            if (f in subset) != ((inner in subset) or (xf in subset)):
                return False
        elif isinstance(f, ast.Globally):
            inner = f.inner
            xg = ast.Next(f)
            if xg not in closure:
                return False
            if (f in subset) != ((inner in subset) and (xg in subset)):
                return False

    return True


def visit_elementary_sets(closure_phi: list[ast.Formula]) -> list[set[ast.Formula]]:
    """Enumerate all subsets of the closure (from `visit_formula`) that are locally consistent."""
    closure = set(closure_phi)
    ordered = sorted(closure, key=_closure_sort_key)
    elementary_sets: list[set[ast.Formula]] = []
    for r in range(len(ordered) + 1):
        for tup in itertools.combinations(ordered, r):
            b = set(tup)
            if is_consistent(b, closure):
                elementary_sets.append(b)
    return elementary_sets


def atoms_true_in_elementary_set(elem: set[ast.Formula]) -> frozenset[str]:
    """
    Atomic propositions satisfied in elem: proposition symbols p with Prop(p) ∈ elem.
    (If Not(p) ∈ elem is also required for consistency when Not(p) is in the closure;
    then p cannot appear here.)
    """
    return frozenset(f.name for f in elem if isinstance(f, ast.Prop))


def atoms_in_closure(closure: set[ast.Formula]) -> frozenset[str]:
    """All proposition names that appear in cl(φ) (as Prop or under Not)."""
    out: set[str] = set()
    for f in closure:
        if isinstance(f, ast.Prop):
            out.add(f.name)
        elif isinstance(f, ast.Not) and isinstance(f.inner, ast.Prop):
            out.add(f.inner.name)
    return frozenset(out)


def _elementary_transition_ok(
    source: set[ast.Formula], target: set[ast.Formula], closure: set[ast.Formula]
) -> bool:
    """
    Single GNBA step relation B → B': Next synchronization and Until obligation carry-over.
    - For every Xψ in closure: ψ ∈ target iff Xψ ∈ source.
    - For every ψ₁ U ψ₂ in closure: if ψ₁ U ψ₂ ∈ source and ψ₂ ∉ source then ψ₁ U ψ₂ ∈ target.
    """
    for f in closure:
        if isinstance(f, ast.Next):
            if (f in source) != (f.inner in target):
                return False
    for f in closure:
        if isinstance(f, ast.Until):
            if f in source and f.right not in source and f not in target:
                return False
    return True


def _accept_elem_with_debug(
    elem: frozenset[ast.Formula],
    until: ast.Formula,
    b: ast.Formula,
) -> bool:
    # For b = !x, use x as complement test instead of building !!x.
    if until not in elem:
        result = True
    elif b in elem:
        result = True
    elif isinstance(b, ast.Not):
        result = b.inner not in elem
    else:
        result = ast.Not(b) not in elem

    # elem_str = ", ".join(sorted(ast.format_formula(x) for x in elem))
    # print(
    #     f"[accept-check] elem={{ {elem_str} }} b={ast.format_formula(b)} result={result}"
    # )
    return result


def generate_accept_family(
    formula: ast.Formula,
    elementary_frozen: list[frozenset[ast.Formula]],
) -> frozenset[int]:
    """
    One generalized-Büchi acceptance set (indices of elementary sets)
    for formula: state j is accepting iff (until ∉ B_j) ∨ (b ∈ B_j).

    - Globally Gψ: b = ¬ψ, until = ¬(Gψ)
    - Finally Fψ: b = ψ, until = Fψ
    - Until ψ₁ U ψ₂: b = ψ₂, until = ψ₁ U ψ₂
    - Other operators: empty set (caller should not append).
    """
    until: ast.Formula
    b: ast.Formula
    if isinstance(formula, ast.Globally):
        if isinstance(formula.inner, ast.Not):
            b = formula.inner.inner
        else:
            b = ast.Not(formula.inner)
        until = ast.Not(formula)
    elif isinstance(formula, ast.Finally):
        b = formula.inner
        until = formula
    elif isinstance(formula, ast.Until):
        b = formula.right
        until = formula
    else:
        return frozenset()

    accepting: set[int] = set()
    for j, elem in enumerate(elementary_frozen):
        if _accept_elem_with_debug(elem, until, b):
            accepting.add(j)
    return frozenset(accepting)


def build_elementary_graph(
    elementary_sets: list[set[ast.Formula]],
    closure: set[ast.Formula],
) -> tuple[list[frozenset[ast.Formula]], list[frozenset[str]], list[list[int]]]:
    """
    Returns frozen elementary sets, AP labels, and successor lists.
    Edge i → j iff `_elementary_transition_ok(B_i, B_j, closure)`.
    """
    frozen = [frozenset(b) for b in elementary_sets]
    ap_labels = [atoms_true_in_elementary_set(b) for b in elementary_sets]
    edges: list[list[int]] = []
    for b in elementary_sets:
        succ = [j for j, b2 in enumerate(elementary_sets) if _elementary_transition_ok(b, b2, closure)]
        edges.append(succ)
    return frozen, ap_labels, edges


class GNBA:
    def __init__(self, ltl_formula: ast.Formula):
        self.formula = ltl_formula
        self.closure_phi = visit_formula(ltl_formula)
        self.closure: set[ast.Formula] = set(self.closure_phi)
        self.elementary_sets: list[set[ast.Formula]] = visit_elementary_sets(self.closure_phi)
        self.elementary_frozen, self.ap_labels, self.edges = build_elementary_graph(
            self.elementary_sets,
            self.closure,
        )
        self.ap_alphabet = atoms_in_closure(self.closure)
        elem = self.elementary_frozen
        # Initial states where the whole formula holds.
        self.initial_states: list[int] = sorted(i for i, b in enumerate(elem) if self.formula in b)
        # Build one acceptance family for each U/F/G node.
        self.accept_families: list[frozenset[int]] = []
        for node in sorted(self.closure, key=_closure_sort_key):
            fam = generate_accept_family(node, elem)
            if fam:
                self.accept_families.append(fam)

    def remove_unreachable(self) -> None:
        """
        Drop GNBA elementary states not reachable from initial (same idea as
        LTL-verifier GNBA::remove_unreachable before transform_to_NBA).
        """
        n = len(self.elementary_frozen)
        if n == 0:
            return
        reach = _forward_reachable(self.edges, self.initial_states)
        if len(reach) == n:
            return
        sorted_old = sorted(reach)
        new_idx = {old: i for i, old in enumerate(sorted_old)}
        new_edges: list[list[int]] = [[] for _ in sorted_old]
        for old_u in sorted_old:
            nu = new_idx[old_u]
            for old_v in self.edges[old_u]:
                if old_v in new_idx:
                    new_edges[nu].append(new_idx[old_v])
            new_edges[nu] = sorted(set(new_edges[nu]))
        new_initial = sorted({new_idx[i] for i in self.initial_states if i in new_idx})
        new_frozen = [self.elementary_frozen[i] for i in sorted_old]
        new_ap = [self.ap_labels[i] for i in sorted_old]
        new_families: list[frozenset[int]] = []
        for fam in self.accept_families:
            nf = frozenset(new_idx[i] for i in fam if i in new_idx)
            if nf:
                new_families.append(nf)
        self.elementary_frozen = new_frozen
        self.ap_labels = new_ap
        self.edges = new_edges
        self.initial_states = new_initial
        self.accept_families = new_families

    def to_nba(self) -> NBA:
        """
        Degeneralize GNBA (F_0,…,F_{m-1}) to a single NBA with Büchi set F'
        (tracker phase0..m-1 cycles when hitting F_i from phase i).
        If m == 0 (no Until), every state is accepting.
        """
        n = len(self.elementary_frozen)
        m = len(self.accept_families)
        if m == 0:
            return NBA(
                n_states=n,
                edges=[sorted(set(row)) for row in self.edges],
                initial_states=list(self.initial_states),
                accept=frozenset(range(n)),
                gnba_state_for_nba_state=tuple(range(n)),
            )

        def idx(q: int, phase: int) -> int:
            return q * m + phase

        edges_nba: list[list[int]] = [[] for _ in range(n * m)]
        for q in range(n):
            for phase in range(m):
                src = idx(q, phase)
                f_i = self.accept_families[phase]
                for q2 in self.edges[q]:
                    if q in f_i:
                        phase2 = (phase + 1) % m
                    else:
                        phase2 = phase
                    edges_nba[src].append(idx(q2, phase2))
        for s in range(len(edges_nba)):
            edges_nba[s] = sorted(set(edges_nba[s]))

        initial = [idx(q, 0) for q in self.initial_states]
        accept = frozenset(idx(q, 0) for q in self.accept_families[0])
        gnba_map = tuple(s // m for s in range(n * m))
        return NBA(
            n_states=n * m,
            edges=edges_nba,
            initial_states=initial,
            accept=accept,
            gnba_state_for_nba_state=gnba_map,
        )


def prune_nba_unreachable(nba: NBA) -> NBA:
    """
    Remove NBA states not reachable from initial (LTL-verifier after transform_to_NBA).
    """
    reach = _forward_reachable(nba.edges, nba.initial_states)
    if len(reach) == nba.n_states:
        return nba
    sorted_old = sorted(reach)
    new_idx = {old: i for i, old in enumerate(sorted_old)}
    new_edges: list[list[int]] = [[] for _ in sorted_old]
    for old_u in sorted_old:
        nu = new_idx[old_u]
        for old_v in nba.edges[old_u]:
            if old_v in new_idx:
                new_edges[nu].append(new_idx[old_v])
        new_edges[nu] = sorted(set(new_edges[nu]))
    new_initial = sorted({new_idx[i] for i in nba.initial_states if i in new_idx})
    new_accept = frozenset(new_idx[i] for i in nba.accept if i in new_idx)
    new_gmap = tuple(nba.gnba_state_for_nba_state[old] for old in sorted_old)
    return NBA(
        n_states=len(sorted_old),
        edges=new_edges,
        initial_states=new_initial,
        accept=new_accept,
        gnba_state_for_nba_state=new_gmap,
    )
