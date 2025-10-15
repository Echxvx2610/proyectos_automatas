# Generated from CSV.g4 by ANTLR 4.13.2
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
    from typing import TextIO
else:
    from typing.io import TextIO


def serializedATN():
    return [
        4,0,6,42,6,-1,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,1,
        0,1,0,1,1,1,1,1,2,1,2,1,3,4,3,21,8,3,11,3,12,3,22,1,4,1,4,1,4,1,
        4,5,4,29,8,4,10,4,12,4,32,9,4,1,4,1,4,1,5,4,5,37,8,5,11,5,12,5,38,
        1,5,1,5,0,0,6,1,1,3,2,5,3,7,4,9,5,11,6,1,0,3,4,0,10,10,13,13,34,
        34,44,44,1,0,34,34,2,0,9,9,32,32,45,0,1,1,0,0,0,0,3,1,0,0,0,0,5,
        1,0,0,0,0,7,1,0,0,0,0,9,1,0,0,0,0,11,1,0,0,0,1,13,1,0,0,0,3,15,1,
        0,0,0,5,17,1,0,0,0,7,20,1,0,0,0,9,24,1,0,0,0,11,36,1,0,0,0,13,14,
        5,13,0,0,14,2,1,0,0,0,15,16,5,10,0,0,16,4,1,0,0,0,17,18,5,44,0,0,
        18,6,1,0,0,0,19,21,8,0,0,0,20,19,1,0,0,0,21,22,1,0,0,0,22,20,1,0,
        0,0,22,23,1,0,0,0,23,8,1,0,0,0,24,30,5,34,0,0,25,26,5,34,0,0,26,
        29,5,34,0,0,27,29,8,1,0,0,28,25,1,0,0,0,28,27,1,0,0,0,29,32,1,0,
        0,0,30,28,1,0,0,0,30,31,1,0,0,0,31,33,1,0,0,0,32,30,1,0,0,0,33,34,
        5,34,0,0,34,10,1,0,0,0,35,37,7,2,0,0,36,35,1,0,0,0,37,38,1,0,0,0,
        38,36,1,0,0,0,38,39,1,0,0,0,39,40,1,0,0,0,40,41,6,5,0,0,41,12,1,
        0,0,0,5,0,22,28,30,38,1,6,0,0
    ]

class CSVLexer(Lexer):

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    T__0 = 1
    T__1 = 2
    T__2 = 3
    TEXT = 4
    STRING = 5
    WS = 6

    channelNames = [ u"DEFAULT_TOKEN_CHANNEL", u"HIDDEN" ]

    modeNames = [ "DEFAULT_MODE" ]

    literalNames = [ "<INVALID>",
            "'\\r'", "'\\n'", "','" ]

    symbolicNames = [ "<INVALID>",
            "TEXT", "STRING", "WS" ]

    ruleNames = [ "T__0", "T__1", "T__2", "TEXT", "STRING", "WS" ]

    grammarFileName = "CSV.g4"

    def __init__(self, input=None, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = LexerATNSimulator(self, self.atn, self.decisionsToDFA, PredictionContextCache())
        self._actions = None
        self._predicates = None


