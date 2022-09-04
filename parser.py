from os import abort
import sys
from tokenController import TokenType
from lex import *
# from statementAnalizer import StatementAnalizer

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
            if self.checkToken(TokenType.Proc):
                self.analizeProc()
                self.nextToken()
            elif Token.checkIfKeyword(self.curToken.text):
                print(self.statement())
                self.nextToken()
            elif self.checkToken(TokenType.EOF):
                print("complied completed")
                break
            else:
                self.abort("Sintax error: Statement not initialize by keyword")

    def analizeProc(self):
        procName = ""
        while self.curToken.text != ';':
            if self.checkToken(TokenType.Proc):
                self.abort("Sintax error: Proc into a proc")
            elif self.checkToken(TokenType.VARIABLE_NAME):
                procName = self.curToken.text
                self.nextToken()
            elif Token.checkIfKeyword(self.curToken.text):
                print(self.statement())
                self.nextToken()
            elif self.curToken.text == "\n":
                self.nextToken()
            elif self.curToken.text == ")" and self.peekToken.text == ";":
                self.nextToken()
                return
            elif self.checkToken(TokenType.EOF):
                self.abort("Sintax Error: Proc never finalize")
            else:
                self.abort("Sintax error: Statement not initialize by keyword")


    def statement(self):
        keyword = self.curToken
        tokenList = []

        if self.checkToken(TokenType.Alter) or self.checkToken(TokenType.IsTrue):
            tokenList.append(self.curToken.text)
            while self.peekToken.text != ')':
                self.nextToken()
                tokenList.append(self.curToken.text)
            tokenList.append(self.peekToken.text)
            return tokenList

        while self.curToken.text != ';':
            if Token.checkIfKeyword(self.curToken.text) and self.curToken.text != keyword.text and not self.checkToken(TokenType.Proc):
                tokenList.append(self.statement()) # Recursive Call
            elif self.checkToken(TokenType.Proc):
                self.abort("Sintax Error: Proc inside a statement")
            elif self.checkToken(TokenType.EOF):
                self.abort("Sintax Error: Statement never finalize")
            elif self.curToken.text != "\n" and self.curToken.text != ";":
                tokenList.append(self.curToken.text)
            self.nextToken()

        return tokenList
        
        
