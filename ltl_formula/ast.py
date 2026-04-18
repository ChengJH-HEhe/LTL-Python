from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Prop:
    name: str


@dataclass(frozen=True)
class Not:
    inner: Formula


@dataclass(frozen=True)
class And:
    left: Formula
    right: Formula


@dataclass(frozen=True)
class Or:
    left: Formula
    right: Formula


@dataclass(frozen=True)
class Implies:
    left: Formula
    right: Formula


@dataclass(frozen=True)
class Until:
    left: Formula
    right: Formula


@dataclass(frozen=True)
class Next:
    inner: Formula


@dataclass(frozen=True)
class Finally:
    inner: Formula


@dataclass(frozen=True)
class Globally:
    inner: Formula


Formula = Union[
    Prop,
    Not,
    And,
    Or,
    Implies,
    Until,
    Next,
    Finally,
    Globally,
]


def intern_formula(f: Formula) -> Formula:
    """Rebind subformulas so each distinct structural shape is a single shared node (DAG / hash cons)."""
    cache: dict[tuple[object, ...], Formula] = {}

    def intern(x: Formula) -> Formula:
        if isinstance(x, Prop):
            k = ("Prop", x.name)
            hit = cache.get(k)
            if hit is not None:
                return hit
            v: Formula = Prop(x.name)
            cache[k] = v
            return v
        if isinstance(x, Not):
            inner = intern(x.inner)
            k = ("Not", inner)
            hit = cache.get(k)
            if hit is not None:
                return hit
            v = Not(inner)
            cache[k] = v
            return v
        if isinstance(x, And):
            left, right = intern(x.left), intern(x.right)
            k = ("And", left, right)
            hit = cache.get(k)
            if hit is not None:
                return hit
            v = And(left, right)
            cache[k] = v
            return v
        if isinstance(x, Or):
            left, right = intern(x.left), intern(x.right)
            k = ("Or", left, right)
            hit = cache.get(k)
            if hit is not None:
                return hit
            v = Or(left, right)
            cache[k] = v
            return v
        if isinstance(x, Implies):
            left, right = intern(x.left), intern(x.right)
            k = ("Implies", left, right)
            hit = cache.get(k)
            if hit is not None:
                return hit
            v = Implies(left, right)
            cache[k] = v
            return v
        if isinstance(x, Until):
            left, right = intern(x.left), intern(x.right)
            k = ("Until", left, right)
            hit = cache.get(k)
            if hit is not None:
                return hit
            v = Until(left, right)
            cache[k] = v
            return v
        if isinstance(x, Next):
            inner = intern(x.inner)
            k = ("Next", inner)
            hit = cache.get(k)
            if hit is not None:
                return hit
            v = Next(inner)
            cache[k] = v
            return v
        if isinstance(x, Finally):
            inner = intern(x.inner)
            k = ("Finally", inner)
            hit = cache.get(k)
            if hit is not None:
                return hit
            v = Finally(inner)
            cache[k] = v
            return v
        if isinstance(x, Globally):
            inner = intern(x.inner)
            k = ("Globally", inner)
            hit = cache.get(k)
            if hit is not None:
                return hit
            v = Globally(inner)
            cache[k] = v
            return v
        raise TypeError(type(x))

    return intern(f)


def format_formula(f: Formula) -> str:
    if isinstance(f, Prop):
        return f.name
    if isinstance(f, Not):
        return f"!({format_formula(f.inner)})"
    if isinstance(f, And):
        return f"(({format_formula(f.left)}) /\\ ({format_formula(f.right)}))"
    if isinstance(f, Or):
        return f"(({format_formula(f.left)}) \\/ ({format_formula(f.right)}))"
    if isinstance(f, Implies):
        return f"(({format_formula(f.left)}) -> ({format_formula(f.right)}))"
    if isinstance(f, Until):
        return f"(({format_formula(f.left)}) U ({format_formula(f.right)}))"
    if isinstance(f, Next):
        return f"X({format_formula(f.inner)})"
    if isinstance(f, Finally):
        return f"F({format_formula(f.inner)})"
    if isinstance(f, Globally):
        return f"G({format_formula(f.inner)})"
    raise TypeError(type(f))
