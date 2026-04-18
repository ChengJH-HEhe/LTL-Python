# Generated from /home/oranjun/LTL-Formula/grammars/LTL.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .LTLParser import LTLParser
else:
    from LTLParser import LTLParser

# This class defines a complete generic visitor for a parse tree produced by LTLParser.

class LTLVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LTLParser#formula.
    def visitFormula(self, ctx:LTLParser.FormulaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#UntilSingle.
    def visitUntilSingle(self, ctx:LTLParser.UntilSingleContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#UntilChain.
    def visitUntilChain(self, ctx:LTLParser.UntilChainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#ImplyRec.
    def visitImplyRec(self, ctx:LTLParser.ImplyRecContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#ImplyAtom.
    def visitImplyAtom(self, ctx:LTLParser.ImplyAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#OrAtom.
    def visitOrAtom(self, ctx:LTLParser.OrAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#OrChain.
    def visitOrChain(self, ctx:LTLParser.OrChainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#AndAtom.
    def visitAndAtom(self, ctx:LTLParser.AndAtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#AndChain.
    def visitAndChain(self, ctx:LTLParser.AndChainContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#Not.
    def visitNot(self, ctx:LTLParser.NotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#Globally.
    def visitGlobally(self, ctx:LTLParser.GloballyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#Finally.
    def visitFinally(self, ctx:LTLParser.FinallyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#Next.
    def visitNext(self, ctx:LTLParser.NextContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#UnaryPass.
    def visitUnaryPass(self, ctx:LTLParser.UnaryPassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#Parens.
    def visitParens(self, ctx:LTLParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LTLParser#Prop.
    def visitProp(self, ctx:LTLParser.PropContext):
        return self.visitChildren(ctx)



del LTLParser