import sys
from tokenController import *

class Lexer:
    def __init__(self, input):
        self.source = input + '\n' # Source code to lex as a string. Append a newline to simplify lexing/parsing the last token/statement.
        self.curChar = ''   # Current character in the string.
        self.curPos = -1    # Current position in the string.
        self.nextChar()
        self.initialParenthesis = 0
        self.finalParenthesis = 0 
        self.newLineCount = 1

    # Process the next character.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            if self.finalParenthesis != self.initialParenthesis:
                self.abort("Sintax error: Parenthesis")
            else:
                self.curChar = '\0'  # EOF
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character.
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]

    # Invalid token found, print error message and exit.
    def abort(self, message):
        raise Exception("Lexer error in line "+ str(self.newLineCount)+". " + message)
		
    # Skip whitespace except newlines, which we will use to indicate the end of a statement.
    def skipWhitespace(self):
        while self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()
		
    # Skip comments in the code.
    def skipComment(self):
        if self.curChar + self.peek() == '-':
            while self.curChar != '\n':
                self.nextChar()

    def getToken(self):
        token = None

        tokenText = ''

        self.skipWhitespace()
        self.skipComment()

        posibleTokens = {
            'ADD' : TokenController.add,
            'SUB' : TokenController.minus,
            'MUL' : TokenController.mul,
            'DIV' : TokenController.div,
            '\n' : TokenController.newLine,
            '>' : TokenController.greater,
            '<' : TokenController.less,
            '==' : TokenController.equalEqual,
            '<>' : TokenController.notEqual,
            '<=' : TokenController.lessEqual,
            '>=' : TokenController.greaterEqual,
            '\0' : TokenController.eof,
            ';' : TokenController.semiColon,
            ',' : TokenController.comma,
            '@' : TokenController.variable,
            '@Principal' : TokenController.principal,
            'New' : TokenController.new,
            'Values' : TokenController.values,
            'Alter' : TokenController.alter,            
            'AlterB' : TokenController.alterB,            
            'MoveRight' : TokenController.moveRight,            
            'MoveLeft' : TokenController.moveLeft,            
            'Then' : TokenController.then,            
            'Else' : TokenController.else_keyword,            
            'While' : TokenController.while_keyword,            
            'When' : TokenController.when,            
            'Case' : TokenController.case,            
            'Hammer' : TokenController.hammer,            
            'Stop' : TokenController.stop,            
            'IsTrue' : TokenController.isTrue,            
            'Repeat' : TokenController.repeat,            
            'Until' : TokenController.until,            
            'PrintValues' : TokenController.printValues,
            'Number' : TokenController.number,
            'String' : TokenController.string,
            'Num' : TokenController.num,
            'Bool' : TokenController.bool,
            '(' : TokenController.initial_parenthesis,
            ')' : TokenController.final_parenthesis,
            'True' : TokenController.true,
            'False' : TokenController.false,
            'Proc' : TokenController.proc,
            'CALL' : TokenController.call,
            'N' : TokenController.n,
            'S' : TokenController.s,
            'E' : TokenController.e,
            'O' : TokenController.o    
        } 

        tokenText = self.curChar
        keyValue = tokenText

        #validations
        if self.curChar == '<' or self.curChar == '>' or self.curChar == '=':
            tokenText =  self.numericConditionals() 
            keyValue = tokenText 
        elif self.curChar.isalpha() or self.curChar =='@': 
            initial = self.curChar 
            tokenText = self.keyWordsOrIdentifiers()
            if initial == '@':
                if tokenText == '@Principal':
                    keyValue = '@Principal'
                else:
                    keyValue = '@'
            else:
                keyValue = tokenText
        elif self.curChar.isdigit():
            tokenText = self.checkNumbers() 
            keyValue = 'Number'
        elif self.curChar == '\"':
            tokenText = self.checkStrings()
            keyValue == 'String'
        elif self.curChar == ',' or self.curChar == ';':
            tokenText = self.checkComaAndSemiColon()
            keyValue = tokenText
        elif self.curChar == ')' or self.curChar == '(':
            self.checkParenthesisCount()
            tokenText = self.curChar
            keyValue = tokenText
        elif self.curChar =='\n':
            keyValue = '\n'
            tokenText = keyValue
            self.newLineCount += 1



        try:
           # print(tokenText)
            controller = posibleTokens.get(keyValue) 
            token = controller(tokenText) 
        except:
            self.abort("Unknown token: " + keyValue)

        self.nextChar()
        return token
            
    def numericConditionals(self):
        tokenText = self.curChar
        if self.peek() == '=':
            self.nextChar()
            tokenText += self.curChar
        elif self.curChar + self.peek() == '<>':
            self.nextChar()
            tokenText += self.curChar
        return tokenText 

    def keyWordsOrIdentifiers(self):
        startPos = self.curPos

        while self.peek().isalnum():
            self.nextChar()

        tokenText = self.source[startPos:self.curPos+1]
        keyword = Token.checkTokenType(tokenText) and Token.checkTokenType(tokenText).name
        
        if keyword == None: # it is a variable 
            return tokenText
        else:
            return keyword

    def checkNumbers(self):
        startPos = self.curPos
        while self.peek().isdigit():
            self.nextChar()
        tokenText = self.source[startPos : self.curPos + 1] # Get the substring.
        return tokenText

    def checkStrings(self):
            # Get characters between quotations.
            self.nextChar()
            startPos = self.curPos

            while self.curChar != '\"':
                # Don't allow special characters in the string. No escape characters, newlines, tabs, or %.
                # We will be using C's printf on this string.
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()

            tokenText = self.source[startPos : self.curPos] # Get the substring.
            return tokenText

    def checkComaAndSemiColon(self):
        tokenText = self.curChar
        return tokenText
    
    def checkParenthesisCount(self):
        if self.curChar == '(':
            self.initialParenthesis += 1
        else:
            self.finalParenthesis += 1
        











