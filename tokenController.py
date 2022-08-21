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

class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    Number = 1
    VARIABLE_NAME = 3
    STRING = 4
	# Keywords.
    New = 101
    Values = 102
    Alter = 103
    AlterB = 104
    MoveRight = 105
    MoveLeft = 106
    Then = 107
    Else = 108
    While = 109
    When = 110
    Case = 111
    Hammer = 112
    Stop = 113
    IsTrue = 114
    Repeat = 115
    Until = 116
    PrintValues = 115
    True_k = 116
    False_k = 117
    Num = 118
    Bool = 119
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
    def checkTokenType(tokenText):
        for kind in TokenType:
            # identifies keywords or operator
            if kind.name == tokenText and kind.value >= 100 :
                return kind.name
            elif kind.name == tokenText+'_k': #check for true and false 
                return tokenText
        return None