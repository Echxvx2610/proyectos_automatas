# Generated from CSV.g4 by ANTLR 4.13.2
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
        4,1,6,39,2,0,7,0,2,1,7,1,2,2,7,2,1,0,1,0,3,0,9,8,0,1,0,1,0,5,0,13,
        8,0,10,0,12,0,16,9,0,1,0,3,0,19,8,0,1,0,3,0,22,8,0,1,0,1,0,1,1,1,
        1,1,1,5,1,29,8,1,10,1,12,1,32,9,1,1,2,1,2,1,2,3,2,37,8,2,1,2,0,0,
        3,0,2,4,0,0,42,0,6,1,0,0,0,2,25,1,0,0,0,4,36,1,0,0,0,6,21,3,2,1,
        0,7,9,5,1,0,0,8,7,1,0,0,0,8,9,1,0,0,0,9,10,1,0,0,0,10,11,5,2,0,0,
        11,13,3,2,1,0,12,8,1,0,0,0,13,16,1,0,0,0,14,12,1,0,0,0,14,15,1,0,
        0,0,15,18,1,0,0,0,16,14,1,0,0,0,17,19,5,1,0,0,18,17,1,0,0,0,18,19,
        1,0,0,0,19,20,1,0,0,0,20,22,5,2,0,0,21,14,1,0,0,0,21,22,1,0,0,0,
        22,23,1,0,0,0,23,24,5,0,0,1,24,1,1,0,0,0,25,30,3,4,2,0,26,27,5,3,
        0,0,27,29,3,4,2,0,28,26,1,0,0,0,29,32,1,0,0,0,30,28,1,0,0,0,30,31,
        1,0,0,0,31,3,1,0,0,0,32,30,1,0,0,0,33,37,5,4,0,0,34,37,5,5,0,0,35,
        37,1,0,0,0,36,33,1,0,0,0,36,34,1,0,0,0,36,35,1,0,0,0,37,5,1,0,0,
        0,6,8,14,18,21,30,36
    ]

class CSVParser ( Parser ):

    grammarFileName = "CSV.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'\\r'", "'\\n'", "','" ]

    symbolicNames = [ "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                      "TEXT", "STRING", "WS" ]

    RULE_csvFile = 0
    RULE_row = 1
    RULE_field = 2

    ruleNames =  [ "csvFile", "row", "field" ]

    EOF = Token.EOF
    T__0=1
    T__1=2
    T__2=3
    TEXT=4
    STRING=5
    WS=6

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class CsvFileContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def row(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CSVParser.RowContext)
            else:
                return self.getTypedRuleContext(CSVParser.RowContext,i)


        def EOF(self):
            return self.getToken(CSVParser.EOF, 0)

        def getRuleIndex(self):
            return CSVParser.RULE_csvFile

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCsvFile" ):
                listener.enterCsvFile(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCsvFile" ):
                listener.exitCsvFile(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCsvFile" ):
                return visitor.visitCsvFile(self)
            else:
                return visitor.visitChildren(self)




    def csvFile(self):

        localctx = CSVParser.CsvFileContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_csvFile)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 6
            self.row()
            self.state = 21
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==1 or _la==2:
                self.state = 14
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,1,self._ctx)
                while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                    if _alt==1:
                        self.state = 8
                        self._errHandler.sync(self)
                        _la = self._input.LA(1)
                        if _la==1:
                            self.state = 7
                            self.match(CSVParser.T__0)


                        self.state = 10
                        self.match(CSVParser.T__1)
                        self.state = 11
                        self.row() 
                    self.state = 16
                    self._errHandler.sync(self)
                    _alt = self._interp.adaptivePredict(self._input,1,self._ctx)

                self.state = 18
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==1:
                    self.state = 17
                    self.match(CSVParser.T__0)


                self.state = 20
                self.match(CSVParser.T__1)


            self.state = 23
            self.match(CSVParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class RowContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def field(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CSVParser.FieldContext)
            else:
                return self.getTypedRuleContext(CSVParser.FieldContext,i)


        def getRuleIndex(self):
            return CSVParser.RULE_row

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterRow" ):
                listener.enterRow(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitRow" ):
                listener.exitRow(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitRow" ):
                return visitor.visitRow(self)
            else:
                return visitor.visitChildren(self)




    def row(self):

        localctx = CSVParser.RowContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_row)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 25
            self.field()
            self.state = 30
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==3:
                self.state = 26
                self.match(CSVParser.T__2)
                self.state = 27
                self.field()
                self.state = 32
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FieldContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser


        def getRuleIndex(self):
            return CSVParser.RULE_field

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)



    class QuotedFieldContext(FieldContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CSVParser.FieldContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def STRING(self):
            return self.getToken(CSVParser.STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterQuotedField" ):
                listener.enterQuotedField(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitQuotedField" ):
                listener.exitQuotedField(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitQuotedField" ):
                return visitor.visitQuotedField(self)
            else:
                return visitor.visitChildren(self)


    class EmptyFieldContext(FieldContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CSVParser.FieldContext
            super().__init__(parser)
            self.copyFrom(ctx)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterEmptyField" ):
                listener.enterEmptyField(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitEmptyField" ):
                listener.exitEmptyField(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitEmptyField" ):
                return visitor.visitEmptyField(self)
            else:
                return visitor.visitChildren(self)


    class TextFieldContext(FieldContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CSVParser.FieldContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def TEXT(self):
            return self.getToken(CSVParser.TEXT, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTextField" ):
                listener.enterTextField(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTextField" ):
                listener.exitTextField(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTextField" ):
                return visitor.visitTextField(self)
            else:
                return visitor.visitChildren(self)



    def field(self):

        localctx = CSVParser.FieldContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_field)
        try:
            self.state = 36
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [4]:
                localctx = CSVParser.TextFieldContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 33
                self.match(CSVParser.TEXT)
                pass
            elif token in [5]:
                localctx = CSVParser.QuotedFieldContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 34
                self.match(CSVParser.STRING)
                pass
            elif token in [-1, 1, 2, 3]:
                localctx = CSVParser.EmptyFieldContext(self, localctx)
                self.enterOuterAlt(localctx, 3)

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





