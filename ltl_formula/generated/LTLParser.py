# Generated from /home/oranjun/LTL-Formula/grammars/LTL.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,12,76,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,5,1,24,8,1,10,1,12,1,27,9,
        1,1,2,1,2,1,2,1,2,1,2,3,2,34,8,2,1,3,1,3,1,3,1,3,1,3,1,3,5,3,42,
        8,3,10,3,12,3,45,9,3,1,4,1,4,1,4,1,4,1,4,1,4,5,4,53,8,4,10,4,12,
        4,56,9,4,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,1,5,3,5,67,8,5,1,6,1,6,
        1,6,1,6,1,6,3,6,74,8,6,1,6,0,3,2,6,8,7,0,2,4,6,8,10,12,0,0,77,0,
        14,1,0,0,0,2,17,1,0,0,0,4,33,1,0,0,0,6,35,1,0,0,0,8,46,1,0,0,0,10,
        66,1,0,0,0,12,73,1,0,0,0,14,15,3,2,1,0,15,16,5,0,0,1,16,1,1,0,0,
        0,17,18,6,1,-1,0,18,19,3,4,2,0,19,25,1,0,0,0,20,21,10,2,0,0,21,22,
        5,1,0,0,22,24,3,4,2,0,23,20,1,0,0,0,24,27,1,0,0,0,25,23,1,0,0,0,
        25,26,1,0,0,0,26,3,1,0,0,0,27,25,1,0,0,0,28,29,3,6,3,0,29,30,5,8,
        0,0,30,31,3,4,2,0,31,34,1,0,0,0,32,34,3,6,3,0,33,28,1,0,0,0,33,32,
        1,0,0,0,34,5,1,0,0,0,35,36,6,3,-1,0,36,37,3,8,4,0,37,43,1,0,0,0,
        38,39,10,2,0,0,39,40,5,7,0,0,40,42,3,8,4,0,41,38,1,0,0,0,42,45,1,
        0,0,0,43,41,1,0,0,0,43,44,1,0,0,0,44,7,1,0,0,0,45,43,1,0,0,0,46,
        47,6,4,-1,0,47,48,3,10,5,0,48,54,1,0,0,0,49,50,10,2,0,0,50,51,5,
        6,0,0,51,53,3,10,5,0,52,49,1,0,0,0,53,56,1,0,0,0,54,52,1,0,0,0,54,
        55,1,0,0,0,55,9,1,0,0,0,56,54,1,0,0,0,57,58,5,5,0,0,58,67,3,10,5,
        0,59,60,5,2,0,0,60,67,3,10,5,0,61,62,5,3,0,0,62,67,3,10,5,0,63,64,
        5,4,0,0,64,67,3,10,5,0,65,67,3,12,6,0,66,57,1,0,0,0,66,59,1,0,0,
        0,66,61,1,0,0,0,66,63,1,0,0,0,66,65,1,0,0,0,67,11,1,0,0,0,68,69,
        5,9,0,0,69,70,3,2,1,0,70,71,5,10,0,0,71,74,1,0,0,0,72,74,5,11,0,
        0,73,68,1,0,0,0,73,72,1,0,0,0,74,13,1,0,0,0,6,25,33,43,54,66,73
    ]

class LTLParser ( Parser ):

    grammarFileName = "LTL.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'U'", "'G'", "'F'", "'X'", "'!'", "'/\\'", 
                     "'\\/'", "'->'", "'('", "')'" ]

    symbolicNames = [ "<INVALID>", "U_OP", "G_MOD", "F_MOD", "X_MOD", "NOT", 
                      "AND", "OR", "IMP", "LPAREN", "RPAREN", "ID", "WS" ]

    RULE_formula = 0
    RULE_untilExpr = 1
    RULE_implyExpr = 2
    RULE_orExpr = 3
    RULE_andExpr = 4
    RULE_unaryExpr = 5
    RULE_primary = 6

    ruleNames =  [ "formula", "untilExpr", "implyExpr", "orExpr", "andExpr", 
                   "unaryExpr", "primary" ]

    EOF = Token.EOF
    U_OP=1
    G_MOD=2
    F_MOD=3
    X_MOD=4
    NOT=5
    AND=6
    OR=7
    IMP=8
    LPAREN=9
    RPAREN=10
    ID=11
    WS=12

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class FormulaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def untilExpr(self):
            return self.getTypedRuleContext(LTLParser.UntilExprContext,0)


        def EOF(self):
            return self.getToken(LTLParser.EOF, 0)

        def getRuleIndex(self):
            return LTLParser.RULE_formula

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFormula" ):
                return visitor.visitFormula(self)
            else:
                return visitor.visitChildren(self)




    def formula(self):

        localctx = LTLParser.FormulaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_formula)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 14
            self.untilExpr(0)
            self.state = 15
            self.match(LTLParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class UntilExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return LTLParser.RULE_untilExpr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class UntilSingleContext(UntilExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.UntilExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def implyExpr(self):
            return self.getTypedRuleContext(LTLParser.ImplyExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUntilSingle" ):
                return visitor.visitUntilSingle(self)
            else:
                return visitor.visitChildren(self)


    class UntilChainContext(UntilExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.UntilExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def untilExpr(self):
            return self.getTypedRuleContext(LTLParser.UntilExprContext,0)

        def U_OP(self):
            return self.getToken(LTLParser.U_OP, 0)
        def implyExpr(self):
            return self.getTypedRuleContext(LTLParser.ImplyExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUntilChain" ):
                return visitor.visitUntilChain(self)
            else:
                return visitor.visitChildren(self)



    def untilExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = LTLParser.UntilExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 2
        self.enterRecursionRule(localctx, 2, self.RULE_untilExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            localctx = LTLParser.UntilSingleContext(self, localctx)
            self._ctx = localctx
            _prevctx = localctx

            self.state = 18
            self.implyExpr()
            self._ctx.stop = self._input.LT(-1)
            self.state = 25
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,0,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = LTLParser.UntilChainContext(self, LTLParser.UntilExprContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_untilExpr)
                    self.state = 20
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 21
                    self.match(LTLParser.U_OP)
                    self.state = 22
                    self.implyExpr() 
                self.state = 27
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,0,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class ImplyExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return LTLParser.RULE_implyExpr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class ImplyRecContext(ImplyExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.ImplyExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def orExpr(self):
            return self.getTypedRuleContext(LTLParser.OrExprContext,0)

        def IMP(self):
            return self.getToken(LTLParser.IMP, 0)
        def implyExpr(self):
            return self.getTypedRuleContext(LTLParser.ImplyExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImplyRec" ):
                return visitor.visitImplyRec(self)
            else:
                return visitor.visitChildren(self)


    class ImplyAtomContext(ImplyExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.ImplyExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def orExpr(self):
            return self.getTypedRuleContext(LTLParser.OrExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitImplyAtom" ):
                return visitor.visitImplyAtom(self)
            else:
                return visitor.visitChildren(self)



    def implyExpr(self):

        localctx = LTLParser.ImplyExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_implyExpr)
        try:
            self.state = 33
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,1,self._ctx)
            if la_ == 1:
                localctx = LTLParser.ImplyRecContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 28
                self.orExpr(0)
                self.state = 29
                self.match(LTLParser.IMP)
                self.state = 30
                self.implyExpr()
                pass

            elif la_ == 2:
                localctx = LTLParser.ImplyAtomContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 32
                self.orExpr(0)
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OrExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return LTLParser.RULE_orExpr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class OrAtomContext(OrExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.OrExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def andExpr(self):
            return self.getTypedRuleContext(LTLParser.AndExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrAtom" ):
                return visitor.visitOrAtom(self)
            else:
                return visitor.visitChildren(self)


    class OrChainContext(OrExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.OrExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def orExpr(self):
            return self.getTypedRuleContext(LTLParser.OrExprContext,0)

        def OR(self):
            return self.getToken(LTLParser.OR, 0)
        def andExpr(self):
            return self.getTypedRuleContext(LTLParser.AndExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOrChain" ):
                return visitor.visitOrChain(self)
            else:
                return visitor.visitChildren(self)



    def orExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = LTLParser.OrExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 6
        self.enterRecursionRule(localctx, 6, self.RULE_orExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            localctx = LTLParser.OrAtomContext(self, localctx)
            self._ctx = localctx
            _prevctx = localctx

            self.state = 36
            self.andExpr(0)
            self._ctx.stop = self._input.LT(-1)
            self.state = 43
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = LTLParser.OrChainContext(self, LTLParser.OrExprContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_orExpr)
                    self.state = 38
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 39
                    self.match(LTLParser.OR)
                    self.state = 40
                    self.andExpr(0) 
                self.state = 45
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class AndExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return LTLParser.RULE_andExpr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)


    class AndAtomContext(AndExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.AndExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def unaryExpr(self):
            return self.getTypedRuleContext(LTLParser.UnaryExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndAtom" ):
                return visitor.visitAndAtom(self)
            else:
                return visitor.visitChildren(self)


    class AndChainContext(AndExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.AndExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def andExpr(self):
            return self.getTypedRuleContext(LTLParser.AndExprContext,0)

        def AND(self):
            return self.getToken(LTLParser.AND, 0)
        def unaryExpr(self):
            return self.getTypedRuleContext(LTLParser.UnaryExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAndChain" ):
                return visitor.visitAndChain(self)
            else:
                return visitor.visitChildren(self)



    def andExpr(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = LTLParser.AndExprContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 8
        self.enterRecursionRule(localctx, 8, self.RULE_andExpr, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            localctx = LTLParser.AndAtomContext(self, localctx)
            self._ctx = localctx
            _prevctx = localctx

            self.state = 47
            self.unaryExpr()
            self._ctx.stop = self._input.LT(-1)
            self.state = 54
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,3,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    localctx = LTLParser.AndChainContext(self, LTLParser.AndExprContext(self, _parentctx, _parentState))
                    self.pushNewRecursionContext(localctx, _startState, self.RULE_andExpr)
                    self.state = 49
                    if not self.precpred(self._ctx, 2):
                        from antlr4.error.Errors import FailedPredicateException
                        raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                    self.state = 50
                    self.match(LTLParser.AND)
                    self.state = 51
                    self.unaryExpr() 
                self.state = 56
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,3,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx


    class UnaryExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return LTLParser.RULE_unaryExpr

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class GloballyContext(UnaryExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.UnaryExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def G_MOD(self):
            return self.getToken(LTLParser.G_MOD, 0)
        def unaryExpr(self):
            return self.getTypedRuleContext(LTLParser.UnaryExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitGlobally" ):
                return visitor.visitGlobally(self)
            else:
                return visitor.visitChildren(self)


    class NotContext(UnaryExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.UnaryExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NOT(self):
            return self.getToken(LTLParser.NOT, 0)
        def unaryExpr(self):
            return self.getTypedRuleContext(LTLParser.UnaryExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNot" ):
                return visitor.visitNot(self)
            else:
                return visitor.visitChildren(self)


    class NextContext(UnaryExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.UnaryExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def X_MOD(self):
            return self.getToken(LTLParser.X_MOD, 0)
        def unaryExpr(self):
            return self.getTypedRuleContext(LTLParser.UnaryExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNext" ):
                return visitor.visitNext(self)
            else:
                return visitor.visitChildren(self)


    class UnaryPassContext(UnaryExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.UnaryExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def primary(self):
            return self.getTypedRuleContext(LTLParser.PrimaryContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitUnaryPass" ):
                return visitor.visitUnaryPass(self)
            else:
                return visitor.visitChildren(self)


    class FinallyContext(UnaryExprContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.UnaryExprContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def F_MOD(self):
            return self.getToken(LTLParser.F_MOD, 0)
        def unaryExpr(self):
            return self.getTypedRuleContext(LTLParser.UnaryExprContext,0)


        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFinally" ):
                return visitor.visitFinally(self)
            else:
                return visitor.visitChildren(self)



    def unaryExpr(self):

        localctx = LTLParser.UnaryExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_unaryExpr)
        try:
            self.state = 66
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [5]:
                localctx = LTLParser.NotContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 57
                self.match(LTLParser.NOT)
                self.state = 58
                self.unaryExpr()
                pass
            elif token in [2]:
                localctx = LTLParser.GloballyContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 59
                self.match(LTLParser.G_MOD)
                self.state = 60
                self.unaryExpr()
                pass
            elif token in [3]:
                localctx = LTLParser.FinallyContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 61
                self.match(LTLParser.F_MOD)
                self.state = 62
                self.unaryExpr()
                pass
            elif token in [4]:
                localctx = LTLParser.NextContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 63
                self.match(LTLParser.X_MOD)
                self.state = 64
                self.unaryExpr()
                pass
            elif token in [9, 11]:
                localctx = LTLParser.UnaryPassContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 65
                self.primary()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PrimaryContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return LTLParser.RULE_primary

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class PropContext(PrimaryContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ID(self):
            return self.getToken(LTLParser.ID, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitProp" ):
                return visitor.visitProp(self)
            else:
                return visitor.visitChildren(self)


    class ParensContext(PrimaryContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a LTLParser.PrimaryContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LPAREN(self):
            return self.getToken(LTLParser.LPAREN, 0)
        def untilExpr(self):
            return self.getTypedRuleContext(LTLParser.UntilExprContext,0)

        def RPAREN(self):
            return self.getToken(LTLParser.RPAREN, 0)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParens" ):
                return visitor.visitParens(self)
            else:
                return visitor.visitChildren(self)



    def primary(self):

        localctx = LTLParser.PrimaryContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_primary)
        try:
            self.state = 73
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [9]:
                localctx = LTLParser.ParensContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 68
                self.match(LTLParser.LPAREN)
                self.state = 69
                self.untilExpr(0)
                self.state = 70
                self.match(LTLParser.RPAREN)
                pass
            elif token in [11]:
                localctx = LTLParser.PropContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 72
                self.match(LTLParser.ID)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[1] = self.untilExpr_sempred
        self._predicates[3] = self.orExpr_sempred
        self._predicates[4] = self.andExpr_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def untilExpr_sempred(self, localctx:UntilExprContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 2)
         

    def orExpr_sempred(self, localctx:OrExprContext, predIndex:int):
            if predIndex == 1:
                return self.precpred(self._ctx, 2)
         

    def andExpr_sempred(self, localctx:AndExprContext, predIndex:int):
            if predIndex == 2:
                return self.precpred(self._ctx, 2)
         




