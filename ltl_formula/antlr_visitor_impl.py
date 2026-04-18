"""
Concrete LtlAstVisitor; requires ANTLR codegen in ltl_formula/generated/ (see tools/gen_antlr.sh).
"""

from __future__ import annotations

import sys
from pathlib import Path

_gen = Path(__file__).resolve().parent / "generated"
if not _gen.is_dir():
    raise ImportError(
        "ANTLR Python output not found at ltl_formula/generated. "
        "Run: bash tools/generate_antlr_parser.sh (Java + antlr-4.13.2-complete.jar required)."
    )
if str(_gen) not in sys.path:
    sys.path.insert(0, str(_gen))

from LTLVisitor import LTLVisitor  # type: ignore  # noqa: E402

from ltl_formula.ast import (  # noqa: E402
    And,
    Finally,
    Formula,
    Globally,
    Implies,
    Next,
    Not,
    Or,
    Prop,
    Until,
)


class LtlAstVisitor(LTLVisitor):
    def visitFormula(self, ctx) -> Formula:
        return self.visit(ctx.untilExpr())

    def visitUntilChain(self, ctx) -> Formula:
        return Until(self.visit(ctx.untilExpr()), self.visit(ctx.implyExpr()))

    def visitUntilSingle(self, ctx) -> Formula:
        return self.visit(ctx.implyExpr())

    def visitImplyRec(self, ctx) -> Formula:
        return Implies(self.visit(ctx.orExpr()), self.visit(ctx.implyExpr()))

    def visitImplyAtom(self, ctx) -> Formula:
        return self.visit(ctx.orExpr())

    def visitOrChain(self, ctx) -> Formula:
        return Or(self.visit(ctx.orExpr()), self.visit(ctx.andExpr()))

    def visitOrAtom(self, ctx) -> Formula:
        return self.visit(ctx.andExpr())

    def visitAndChain(self, ctx) -> Formula:
        return And(self.visit(ctx.andExpr()), self.visit(ctx.unaryExpr()))

    def visitAndAtom(self, ctx) -> Formula:
        return self.visit(ctx.unaryExpr())

    def visitNot(self, ctx) -> Formula:
        return Not(self.visit(ctx.unaryExpr()))

    def visitGlobally(self, ctx) -> Formula:
        return Globally(self.visit(ctx.unaryExpr()))

    def visitFinally(self, ctx) -> Formula:
        return Finally(self.visit(ctx.unaryExpr()))

    def visitNext(self, ctx) -> Formula:
        return Next(self.visit(ctx.unaryExpr()))

    def visitUnaryPass(self, ctx) -> Formula:
        return self.visit(ctx.primary())

    def visitParens(self, ctx) -> Formula:
        return self.visit(ctx.untilExpr())

    def visitProp(self, ctx) -> Formula:
        return Prop(ctx.ID().getText())
