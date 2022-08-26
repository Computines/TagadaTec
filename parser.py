from os import abort
import sys
from lex import *
from statementAnalizer import StatementAnalizer

# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer

        self.symbols = set()    # Variables declared so far.
        self.labelsDeclared = set() # Labels declared so far.
        self.labelsGotoed = set() # Labels goto'ed so far.

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    # Call this twice to initialize current and peek.

    # Return true if the current token matches.
    def checkToken(self, kind):
        return kind == self.curToken.kind

    # Return true if the next token matches.
    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    # Try to match current token. If not, error. Advances the current token.
    def match(self, kind):
        if not self.checkToken(kind):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()
        
    # Advances the current token.
    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        # No need to worry about passing the EOF, lexer handles that.

    def abort(self, message):
        sys.exit("Error. " + message)

    def program(self):
        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
            # Since some newlines are required in our grammar, need to skip the excess.
            while self.checkToken(TokenType.NEWLINE):
                self.nextToken()

            #print(self.curToken.text)
            if Token.checkIfKeyword(self.curToken.text):
                self.statement()
            elif self.checkToken(TokenType.EOF):
                print("complied completed")
                break
            else:
                self.abort("Sintax error: Statement not initialize by keyword")

    def statement(self):
        keyword = self.curToken
        tokenList = []

        while self.curToken.text != ';':
            # print(self.curToken.text)
            if self.curToken.text != "\n" and self.curToken.text != ";":
                tokenList.append(self.curToken.text)
            if self.checkToken(TokenType.Alter) or self.checkToken(TokenType.IsTrue):
                while self.peekToken.text != ')':
                    self.nextToken()
                    tokenList.append(self.curToken.text)
                tokenList.append(self.peekToken.text)
                break
            if Token.checkIfKeyword(self.peekToken.text):
                self.nextToken()
                tokenList.append(self.statement().text)
                continue
            self.nextToken()
            # print(self.curToken.text)
        # if not StatementAnalizer.analize(tokenList):
        #     self.abort("Sintax Error")
        # if true :
                # Emitter(Lista)
        self.nextToken()
        print(tokenList)
        return keyword
        
        
