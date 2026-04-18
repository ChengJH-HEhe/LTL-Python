from ltl_formula.ast import (
    And,
    Finally,
    Formula,
    Globally,
    Implies,
    Not,
    Next,
    Or,
    Prop,
    Until,
    format_formula,
    intern_formula,
)
from ltl_formula.antlr_parse import parse_ltl_antlr
from ltl_formula.benchmark_io import BenchmarkSpec, load_benchmark_file, parse_benchmark_text
from ltl_formula.ts_io import TransitionSystem, ap_index, load_ts_file, parse_ts_text
from ltl_formula.util import strip_state_prefix


def parse_ltl(text: str) -> Formula:
    """Parse an LTL formula string into an AST (requires `ltl_formula/generated/` from ANTLR)."""
    return intern_formula(parse_ltl_antlr(text))


__all__ = [
    "parse_ltl",
    "parse_ltl_antlr",
    "parse_ts_text",
    "load_ts_file",
    "TransitionSystem",
    "ap_index",
    "parse_benchmark_text",
    "load_benchmark_file",
    "BenchmarkSpec",
    "strip_state_prefix",
    "format_formula",
    "intern_formula",
    "Formula",
    "Prop",
    "Not",
    "And",
    "Or",
    "Implies",
    "Until",
    "Next",
    "Finally",
    "Globally",
]
