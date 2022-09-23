from os import abort, stat
from pickletools import read_int4
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
        self.expectedGlobal = []
        self.procs = []

        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()    # Call this twice to initialize current and peek.

        self.newLineCounter = 1 

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

    def abort(self, message, type= "line"):
        if type == "line":
            raise Exception("Parser error in line "+ str(self.newLineCounter) +". "+ message)
        else:
            raise Exception("Parser error. "+message)
    def existPrincipal(self):
        if not "@principal" in self.procs:
            self.abort("@principal proc not found","")

    def globalVarsCheck(self):
        for var in self.expectedGlobal:
            # print(var)
            if not (var[0] in self.variables.keys() and (self.variables[var[0]][0] == "@principal" or self.variables[var[0]][0] == "noProc")):
                self.abort(f"Variable {var[0]} not initialized","")

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
                statement = self.statement("noProc")
                listOfTokens = self.convertTokenToText(statement)
                self.callTester(listOfTokens)
                self.emitter.emitStatement(listOfTokens)
                self.nextToken()
            elif self.checkToken(TokenType.EOF):
                self.existPrincipal()
                self.globalVarsCheck()
                self.emitter.writeFile()
                print("complied completed")
                # print(self.newLineCounter)
                break
            else:
                self.abort("Sintax error: Statement not initialized by keyword","")

    def callTester(self, listOfTokens):
        if listOfTokens[0] == 'CALL':
            if listOfTokens[2] != '@principal':
                self.abort('Statement out of procedure, only call principal can be out of procedure')


        

    def controlNew(self, statement: list, procName: str):
        if ((statement[4].text == "Bool" and (statement[6].kind == TokenType.true or statement[6].kind == TokenType.false)) or \
                statement[4].text == "Num" and statement[6].text.isdigit()) and \
                (not statement[1].text in self.variables.keys() or self.variables[statement[1].text][0] != procName):
            self.variables[statement[1].text] = (procName, statement[4].text)
        elif statement[1].text in self.variables.keys():
            self.abort("Variable " + statement[1].text + " is already defined")
        else:
            self.abort("Data type does not match with initialized type")

    def controlValues(self, statement: list, procName: str):
        for variable in self.variables.items():
            # print(variable)
            if variable[0] == statement[2].text and variable[1][0] == procName:
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
            self.expectedGlobal.append((statement[2].text, procName))

    def controlAlter(self, statement: list, procName: str):
        for variable in self.variables.items():
            if variable[0] == statement[2].text and variable[1][0] == procName:
                if variable[1][1] == "Num":
                    break
                else:
                    self.abort("Data type does not match with variable's type")
        else:
            self.expectedGlobal.append((statement[2].text, procName))

    def controlAlterB(self, statement: list, procName: str):
        for variable in self.variables.items():
            if variable[0] == statement[2].text and variable[1][0] == procName:
                if variable[1][1] == "Bool":
                    break
                else:
                    self.abort("Data type does not match with variable's type")
        else:
            self.expectedGlobal.append((statement[2].text, procName))

    def controlIsTrue(self, statement: list, procName: str):
        for variable in self.variables.items():
            if variable[0] == statement[2].text and variable[1][0] == procName:
                if variable[1][1] == "Bool":
                    break
                else:
                    self.abort("Data type does not match with variable's type")
        else:
            self.expectedGlobal.append((statement[2].text, procName))

    def controlUntil(self, statement: list, procName: str):
        for variable in self.variables.items():
            if variable[0] == statement[-3].text and variable[1][0] == procName:
                if (variable[1][1] == "Bool" and (statement[-1].kind == TokenType.true or statement[-1].kind == TokenType.false)) or \
                    (variable[1][1] == "Num" and statement[-1].kind == TokenType.Number):
                    break
                else:
                    self.abort("Data type does not match with variable's type")
        else:
            self.expectedGlobal.append((statement[-3].text, procName))

    def controlWhile(self, statement: list, procName: str):
        for variable in self.variables.items():
            if isinstance(statement[1], list) or variable[0] == statement[1].text and variable[1][0] == procName:
                if isinstance(statement[1], list) or (variable[1][1] == "Bool" and (statement[3].kind == TokenType.true or statement[3].kind == TokenType.false)) or \
                    (variable[1][1] == "Num" and statement[3].kind == TokenType.Number):
                    break
                else:
                    self.abort("Data type does not match with variable's type")
        else:
            self.expectedGlobal.append((statement[1].text, procName))
    
    def controlCaseWhen(self, statement: list, procName: str):
        for variable in self.variables.items():
            if isinstance(statement[2], list) or variable[0] == statement[3].text and variable[1][0] == procName:
                if isinstance(statement[2], list) or (variable[1][1] == "Bool" and (statement[5].kind == TokenType.true or statement[5].kind == TokenType.false)) or \
                    (variable[1][1] == "Num" and statement[5].kind == TokenType.Number):
                    break
                else:
                    self.abort("Data type does not match with variable's type")
        else:
            self.expectedGlobal.append((statement[3].text, procName))

    def controlCase(self, statement: list, procName: str):
        print(self.convertTokenToText(statement))
        for variable in self.variables.items():
            if variable[0] == statement[1].text and variable[1][0] == procName:
                
                break
        else:
            self.expectedGlobal.append((statement[1].text, procName))

#check this
    def controlPrintValues(self, statement: list, procName: str):
        # print(self.convertTokenToText(statement))
        innerPrint = statement[2:-1]
        for i in range(0,len(innerPrint),2):
            if innerPrint[i].kind == TokenType.VARIABLE_NAME and \
                innerPrint[i].text in self.variables.keys():
                pass
            elif innerPrint[i].kind == TokenType.VARIABLE_NAME:
                self.expectedGlobal.append((innerPrint[i].text, procName))


    def controlVariables(self, statement: list, procName: str):
        if statement[0].kind == TokenType.New:
            self.controlNew(statement, procName)
                
        elif statement[0].kind == TokenType.Values:
            self.controlValues(statement, procName)

        elif statement[0].kind == TokenType.Alter:
            self.controlAlter(statement, procName)

        elif statement[0].kind == TokenType.AlterB:
            self.controlAlterB(statement, procName)

        elif statement[0].kind == TokenType.IsTrue:
            self.controlIsTrue(statement, procName)

        elif statement[0].kind == TokenType.Until:
            self.controlUntil(statement, procName)

        elif statement[0].kind == TokenType.While:
            self.controlWhile(statement, procName)

        elif statement[0].kind == TokenType.Case and statement[1].kind == TokenType.When:
            self.controlCaseWhen(statement, procName)
        
        elif statement[0].kind == TokenType.Case:
            self.controlCase(statement, procName)

        elif statement[0].kind == TokenType.PrintValues:
            self.controlPrintValues(statement, procName)

    def analizeProc(self):
        # Proc Header Structure Seek
        self.nextToken() # Skip Proc Token
        procName = self.curToken.text # Save the Proc Name
        
        if procName in self.procs:
            self.abort("Proc " + procName + " is defined more than once","")
        else:
            self.procs.append(procName)

        self.nextToken() # Skip name token
        self.nextToken() # Skip ( Token


        self.emitter.emitStatement(['Proc', procName, '('])

        while self.curToken.text != ';':
            if self.checkToken(TokenType.Proc):
                self.abort("Sintax error: Proc into a proc","")
            elif self.checkToken(TokenType.VARIABLE_NAME):
                procName = self.curToken.text
                self.nextToken()
            elif Token.checkIfKeyword(self.curToken.text):
                curStatement = self.statement(procName)
                listOfTokens = self.convertTokenToText(curStatement)
                # print(listOfTokens)
                self.emitter.emitStatement(listOfTokens)
                self.nextToken()
            elif self.curToken.text == "\n":
                self.newLineCounter += 1
                # print("proc", self.newLineCounter)
                self.nextToken()
            elif self.curToken.text == ")" and self.peekToken.text == ";":
                self.nextToken()
                break
            elif self.checkToken(TokenType.EOF):
                self.abort("Sintax error: Proc never finalized","")
            else:
                self.abort("Sintax error: Statement not initialized by keyword")

        self.emitter.emitStatement(['EndProc'])

    def statement(self, procName):
        keyword = self.curToken
        tokenList = []

        if self.checkToken(TokenType.Alter) or self.checkToken(TokenType.IsTrue):
            tokenList.append(self.curToken)
            while self.peekToken.text != ')':
                self.nextToken()
                tokenList.append(self.curToken)
            self.nextToken()
            tokenList.append(self.curToken)
            if not StatementAnalizer.analize(tokenList):
                self.abort("Sintax error")
            self.controlVariables(tokenList, procName)
            return tokenList

        while self.curToken.text != ';':
            if Token.checkIfKeyword(self.curToken.text) and self.curToken.text != keyword.text and not self.checkToken(TokenType.Proc):
                tokenList.append(self.statement(procName)) # Recursive Call
            elif self.checkToken(TokenType.Proc):
                self.abort("Sintax error: Proc inside a statement","")
            elif self.checkToken(TokenType.EOF):
                self.abort("Sintax Error: Statement never finalized","")
            elif self.curToken.text == "\n":
                self.newLineCounter += 1
            elif self.curToken.text != "\n" and self.curToken.text != ";":
                tokenList.append(self.curToken)
            self.nextToken()

        if not StatementAnalizer.analize(tokenList):
            self.abort("Sintax error")
        

        self.controlVariables(tokenList, procName)

        return tokenList
        
    def convertTokenToText(self, listOfTokens):
        result = []
        for token in listOfTokens:
            if isinstance(token,list):
                result.append(self.convertTokenToText(token))
            else:
                result.append(token.text)
        return result
    
