"""
Parse LTL using ANTLR-generated code in ltl_formula/generated/.

1. Put antlr4-4.13.2-complete.jar in tools/ (or set ANTLR_JAR to any 4.13.x complete jar).
2. Run: bash tools/generate_antlr_parser.sh (or tools/gen_antlr.sh)
3. pip install -r requirements.txt
"""

from __future__ import annotations

from importlib import import_module
from pathlib import Path

from antlr4 import CommonTokenStream, InputStream

from ltl_formula.ast import Formula


def parse_ltl_antlr(text: str) -> Formula:
    gen = Path(__file__).resolve().parent / "generated"
    if not gen.is_dir():
        raise FileNotFoundError(
            "Missing ltl_formula/generated — run: bash tools/generate_antlr_parser.sh"
        )

    from ltl_formula.antlr_visitor_impl import LtlAstVisitor

    lexer_mod = import_module("LTLLexer")
    parser_mod = import_module("LTLParser")
    raw = text.strip()
    lexer = getattr(lexer_mod, "LTLLexer")(InputStream(raw))
    parser = getattr(parser_mod, "LTLParser")(CommonTokenStream(lexer))
    tree = parser.formula()
    if parser.getNumberOfSyntaxErrors() > 0:
        raise ValueError(
            f"LTL parse failed ({parser.getNumberOfSyntaxErrors()} syntax error(s)): {raw!r}"
        )
    out = LtlAstVisitor().visit(tree)
    if out is None:
        raise ValueError(f"LTL visitor returned None for: {raw!r}")
    return out
