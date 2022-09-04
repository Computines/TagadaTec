import enum
from tkinter.messagebox import RETRY 

class TokenController:
    def __init__(self):
        pass

    @staticmethod
    def add(tokenText):
        return Token(tokenText, TokenType.ADD)

    @staticmethod
    def minus(tokenText):
        return Token(tokenText, TokenType.SUB)

    @staticmethod
    def mul(tokenText):
        return Token(tokenText, TokenType.MUL)

    @staticmethod
    def div(tokenText):
        return Token(tokenText, TokenType.DIV)

    @staticmethod
    def newLine(tokenText):
        return Token(tokenText, TokenType.NEWLINE)    
    
    @staticmethod
    def greater(tokenText):
        return Token(tokenText, TokenType.GREATER)
    
    @staticmethod
    def greaterEqual(tokenText):
        return Token(tokenText, TokenType.GREATER_EQUAL)

    @staticmethod
    def less(tokenText):
        return Token(tokenText, TokenType.LESS)

    @staticmethod
    def lessEqual(tokenText):
        return Token(tokenText, TokenType.LESS_EQUAL)

    @staticmethod
    def notEqual(tokenText):
        return Token(tokenText, TokenType.NOT_EQUAL)

    @staticmethod
    def equalEqual(tokenText):
        return Token(tokenText, TokenType.EQUAL_EQUAL)

    @staticmethod
    def eof(tokenText):
        return Token('',TokenType.EOF)

    @staticmethod
    def semiColon(tokenText):
        return Token(tokenText, TokenType.SEMI_COLON)

    @staticmethod
    def variable(tokenText):
        return Token(tokenText, TokenType.VARIABLE_NAME)

    @staticmethod
    def new(tokenText):
        return Token(tokenText, TokenType.New)

    @staticmethod
    def values(tokenText):
        return Token(tokenText, TokenType.Values)

    @staticmethod
    def alter(tokenText):
        return Token(tokenText, TokenType.Alter)

    @staticmethod
    def alterB(tokenText):
        return Token(tokenText, TokenType.AlterB)

    @staticmethod
    def moveRight(tokenText):
        return Token(tokenText, TokenType.MoveRight)

    @staticmethod
    def moveLeft(tokenText):
        return Token(tokenText, TokenType.MoveLeft)

    @staticmethod
    def hammer(tokenText):
        return Token(tokenText, TokenType.Hammer)

    @staticmethod
    def stop(tokenText):
        return Token(tokenText, TokenType.Stop)

    @staticmethod
    def isTrue(tokenText):
        return Token(tokenText, TokenType.IsTrue)

    @staticmethod
    def repeat(tokenText):
        return Token(tokenText, TokenType.Repeat)

    @staticmethod
    def until(tokenText):
        return Token(tokenText, TokenType.Until)

    @staticmethod
    def while_keyword(tokenText):
        return Token(tokenText, TokenType.While)

    @staticmethod
    def case(tokenText):
        return Token(tokenText, TokenType.Case)

    @staticmethod
    def when(tokenText):
        return Token(tokenText, TokenType.When)

    @staticmethod
    def then(tokenText):
        return Token(tokenText, TokenType.Then)

    @staticmethod
    def else_keyword(tokenText):
        return Token(tokenText, TokenType.Else)

    @staticmethod
    def printValues(tokenText):
        return Token(tokenText, TokenType.PrintValues)

    @staticmethod
    def number(tokenText):
        return Token(tokenText, TokenType.Number)

    @staticmethod
    def string(tokenText):
        return Token(tokenText, TokenType.STRING)

    @staticmethod
    def comma(tokenText):
        return Token(tokenText, TokenType.COMMA)

    @staticmethod
    def num(tokenText):
        return Token(tokenText, TokenType.Num)

    @staticmethod
    def bool(tokenText):
        return Token(tokenText, TokenType.Bool)

    @staticmethod
    def initial_parenthesis(tokenText):
        return Token(tokenText, TokenType.INITIAL_PARENTESIS)
    
    @staticmethod
    def final_parenthesis(tokenText):
        return Token(tokenText, TokenType.FINAL_PARENTESIS)

    @staticmethod
    def true(tokenText):
        return Token(tokenText, TokenType.true)

    @staticmethod
    def false(tokenText):
        return Token(tokenText, TokenType.false)

    @staticmethod
    def principal(tokenText):
        return Token(tokenText, TokenType.Principal)

    @staticmethod
    def call(tokenText):
        return Token(tokenText, TokenType.CALL)

    @staticmethod
    def proc(tokenText):
        return Token(tokenText, TokenType.Proc)

    @staticmethod
    def e(tokenText):
        return Token(tokenText, TokenType.E)

    @staticmethod
    def o(tokenText):
        return Token(tokenText, TokenType.O)

    @staticmethod
    def s(tokenText):
        return Token(tokenText, TokenType.S)

    @staticmethod
    def n(tokenText):
        return Token(tokenText, TokenType.N)

    @staticmethod
    def Break(tokenText):
        return Token(tokenText, TokenType.Break)

class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    Number = 1
    VARIABLE_NAME = 2
    STRING = 3
	# Keywords.
    New = 101
    Values = 102
    Alter = 103
    AlterB = 104
    MoveRight = 105
    MoveLeft = 106
    While = 107
    Case = 108
    Hammer = 109
    Stop = 110
    IsTrue = 111
    Repeat = 112
    Until = 113
    PrintValues = 114
    Proc = 115
    CALL = 116
    Principal = 117
    Break = 118
	# Operators.
    EQUAL = 201  
    ADD = 202
    SUB = 203
    MUL = 204
    DIV = 205
    EQUAL_EQUAL = 206
    NOT_EQUAL = 207
    LESS = 208
    LESS_EQUAL = 209
    GREATER = 210
    GREATER_EQUAL = 211
    SEMI_COLON = 212
    INITIAL_PARENTESIS = 213
    FINAL_PARENTESIS = 214
    COMMA = 215
    true = 216
    false = 217
    Num = 218
    Bool = 219
    When = 220
    Then = 221
    Else = 222
    #positions
    N = 301
    S = 302
    E = 303
    O = 304



class Token:   
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText   # The token's actual text. Used for identifiers, strings, and numbers.
        self.kind = tokenKind   # The TokenType that this token is classified as.
        
    @staticmethod
    def checkTokenType(tokenText, margin = 100):
        for kind in TokenType:
            # identifies keywords or operator
            if kind.name == tokenText and kind.value >= margin :
                return kind
            elif kind.name == tokenText: #check for true and false 
                return kind
        return None

    @staticmethod
    def checkIfKeyword(tokenText):
        for kind in TokenType:
            # identifies keywords or operator
            if kind.name == tokenText and kind.value >= 100 and kind.value < 200 :
                return True
        return False