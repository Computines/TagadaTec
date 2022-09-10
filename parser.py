import sys
from statementAnalizer import StatementAnalizer
from tokenController import TokenType, Token
from lex import *
# from statementAnalizer import StatementAnalizer

# Parser object keeps track of current token and checks if the code matches the grammar.
class Parser:
    def __init__(self, lexer, emitter):
        self.lexer = lexer
        self.emitter = emitter

        self.symbols = set()    # Variables declared so far.
        self.labelsDeclared = set() # Labels declared so far.
        self.labelsGotoed = set() # Labels goto'ed so far.

        self.variables = {}

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    # Call this twice to initialize current and peek.

        self.newLineCounter = 0 

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
        #while not self.checkToken(TokenType.EOF):
        while True:
            # Since some newlines are required in our grammar, need to skip the excess.
            while self.checkToken(TokenType.NEWLINE):
                self.newLineCounter += 1
                self.nextToken()

            #print(self.curToken.text)
            if self.checkToken(TokenType.Proc):
                self.analizeProc()
                self.nextToken()
            elif Token.checkIfKeyword(self.curToken.text):
                statement = self.statement()
                self.controlVariables(statement, "noProc")
                StatementAnalizer.analize(statement)
                listOfTokens = self.convertTokenToText(statement)
                self.emitter.emitStatement(listOfTokens)
                self.nextToken()
            elif self.checkToken(TokenType.EOF):
                self.emitter.writeFile()
                print("complied completed")
                print(self.newLineCounter)
                break
            else:
                self.abort("Sintax error: Statement not initialize by keyword")

    def controlVariables(self, statement: list, procName: str):
        if statement[0].kind == TokenType.New:
            if (statement[4].text == "Bool" and (statement[6].kind == TokenType.true or statement[6].kind == TokenType.false)) or \
                statement[4].text == "Num" and statement[6].text.isdigit():
                self.variables[statement[1].text] = (procName, statement[4].text)
            else:
                self.abort("Data type does not match with initialize type")
        elif statement[0].kind == TokenType.Values:
            for variable in self.variables.items():
                if variable[0] == statement[2].text:
                    if isinstance(statement[4], list) and variable[1][1] == "Num":
                        self.controlVariables(statement[4], procName)
                        break
                    elif statement[4].kind == TokenType.Number and variable[1][1] == "Num":
                        break
                    elif (statement[4].kind == TokenType.true or statement[4].kind == TokenType.false) and variable[1][1] == "Bool":
                        break
                    else:
                        self.abort("Data type does not match with variable's type")
            else:
                self.abort(f"Variable {statement[2].text} not initialized")
        elif statement[0].kind == TokenType.Alter:
            for variable in self.variables.items():
                if variable[0] == statement[2].text:
                    if variable[1][1] == "Num":
                        break
                    else:
                        self.abort("Data type does not match with variable's type")
            else:
                self.abort(f"Variable {statement[2].text} not initialized")
        elif statement[0].kind == TokenType.AlterB:
            for variable in self.variables.items():
                if variable[0] == statement[2].text:
                    if variable[1][1] == "Bool":
                        break
                    else:
                        self.abort("Data type does not match with variable's type")
            else:
                self.abort(f"Variable {statement[2].text} not initialized")

    def analizeProc(self):
        # Proc Header Structure Seek
        self.nextToken() # Skip Proc Token
        procName = self.curToken.text # Save the Proc Name
        self.nextToken() # Skip name token
        self.nextToken() # Skip ( Token


        self.emitter.emitStatement(['Proc', procName, '('])

        while self.curToken.text != ';':
            if self.checkToken(TokenType.Proc):
                self.abort("Sintax error: Proc into a proc")
            elif self.checkToken(TokenType.VARIABLE_NAME):
                procName = self.curToken.text
                self.nextToken()
            elif Token.checkIfKeyword(self.curToken.text):
                curStatement = self.statement()
                self.controlVariables(curStatement, procName)
                listOfTokens = self.convertTokenToText(curStatement)
                self.emitter.emitStatement(listOfTokens)
                self.nextToken()
            elif self.curToken.text == "\n":
                self.newLineCounter += 1
                print("proc", self.newLineCounter)
                self.nextToken()
            elif self.curToken.text == ")" and self.peekToken.text == ";":
                self.nextToken()
                break
            elif self.checkToken(TokenType.EOF):
                self.abort("Sintax Error: Proc never finalize")
            else:
                self.abort("Sintax error: Statement not initialize by keyword")

        self.emitter.emitStatement(['EndProc'])

    def statement(self):
        keyword = self.curToken
        tokenList = []

        if self.checkToken(TokenType.Alter) or self.checkToken(TokenType.IsTrue):
            tokenList.append(self.curToken)
            while self.peekToken.text != ')':
                self.nextToken()
                tokenList.append(self.curToken)
            tokenList.append(self.peekToken)
            StatementAnalizer.analize(tokenList)
            # StatementAnalizer
            return tokenList

        while self.curToken.text != ';':
            if Token.checkIfKeyword(self.curToken.text) and self.curToken.text != keyword.text and not self.checkToken(TokenType.Proc):
                tokenList.append(self.statement()) # Recursive Call
            elif self.checkToken(TokenType.Proc):
                self.abort("Sintax Error: Proc inside a statement")
            elif self.checkToken(TokenType.EOF):
                self.abort("Sintax Error: Statement never finalize")
            elif self.curToken.text == "\n":
                self.newLineCounter += 1
            elif self.curToken.text != "\n" and self.curToken.text != ";":
                tokenList.append(self.curToken)
            self.nextToken()

        StatementAnalizer.analize(tokenList)
        # StatementAnalizer
        
        return tokenList
        
    def convertTokenToText(self, listOfTokens):
        result = []
        for token in listOfTokens:
            if isinstance(token,list):
                result.append(self.convertTokenToText(token))
            else:
                result.append(token.text)
        return result
    
