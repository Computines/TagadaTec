import sys
from tabnanny import check
from turtle import pos
from urllib.parse import ParseResultBytes

# ['New', '@variable', ',', '(', 'Num', ',', '5', ')']
# ['Alter', '(', '@variable1', ',', 'SUB', ',', '3', ')']
# ['Values', '(', '@variable2', ',', '51', ')']
# ['Until', '(', '[MoveRight]', ')', '@variable3', operador, '@variable4' ]
# ['Case', '@mellamocarlos', 'When', '1', 'Then', '(', 'MoveRight', 'MoveLeft', 'MoveLeft', ')', 'When', '2', 'Then', '(', 'MoveLeft', ')']
# ['Case', 'When', '(', '@varible1', '>=', '5', ')', 'Then', '(', ['MoveRight'], ')', 'Else', '(', ['MoveLeft'], ')']

class Emitter:

    def __init__(self, path) -> None:
        self.code = ""
        self.path = path
        self.currentToken = None
        self.nextToken = None
        self.localVariables = []
        self.globalVariables = []
        self.identation = 0

    def abort(self, message):
        sys.exit("Error. " + message)

    def emitLine(self, line):
        self.code += line + '\n'

    def emitIdentation(self):
        self.code += "    " * self.identation

    def writeFile(self):
        with open(self.path, 'w') as file:
            file.write(self.code)

    def commonFuntions(self):
        self.emitLine("true = True")
        self.emitLine("false = False")
        self.emitFuntions()

    def newVariable (self, input):
        variableName = self.getVariableName(input, 1, True)
        variableValue = input[6]

        if variableName not in self.globalVariables:
            self.globalVariables.append(variableName)
            line = variableName + ' = ' + variableValue
            self.emitLine(line)
        else:
            self.abort("Redefinition of variable " + variableName)

    def checkVariableExistance(self, variableName):
        if variableName not in self.globalVariables:
            self.abort("Not declared " + variableName)
        return True

    def getVariableName(self, input, position, inNewVariable):
        if inNewVariable :
            return input[position][1:]
        else:
            variableName = input[position][1:]
            if self.checkVariableExistance(variableName):
                return variableName
            else:
                self.abort("Variable does not exist")

    def alterVariable(self, input):
        operators = {
            'ADD': '+',
            'SUB' : '-',
            'MUL' : '*',
            'DIV' : '/'
        }

        variableName = self.getVariableName(input, 2, False)
        operator = operators.get(input[4])

        if self.checkVariableExistance(variableName):
            return variableName + operator + input[6]

    def valuesStatement(self, input):
        variableName = self.getVariableName(input, 2, False)

        if self.checkVariableExistance(variableName):
            if isinstance(input[4], list):
                line = variableName + ' ' + '= ' + self.alterVariable(input[4])
            else:
                line = variableName + ' ' + '= ' + input[4]

            self.emitLine(line)

    def untilStatement(self, input):
        initialPosition = 1
        self.identation -= 1
        self.checkIntructions(initialPosition, input)
        self.identation = 0
        condition = self.getCondition(-3, -2, -1, input)
        self.emitLine('while ' + condition + ':')
        self.checkIntructions(initialPosition, input)
        

    def whileStatement(self, input):
        if isinstance(input[1], list): #check if it is IsTrue
            if input[1][0] == 'IsTrue':
                condition = self.isTrue(input[1])
                self.emitLine('while ' + condition + ':')  
                initialPosition = 2
                self.checkIntructions(initialPosition, input)

        else:
            condition = self.getCondition(1,2,3,input)
            self.emitLine('while ' + condition + ':')  
            initialPosition = 4

            self.checkIntructions(initialPosition, input)

    def checkIntructions(self, initialPosition, input):
        for positions in range(initialPosition, len(input)):
            if isinstance(input[positions], list):
                self.emitIdentation()
                if input[positions][0] == 'Values':
                    self.valuesStatement(input[positions]) 
                elif input[positions][0] == 'MoveRight':
                    self.emitLine("moveRight()")
                    #self.moveRight()
                elif input[positions][0] == 'MoveLeft':
                    self.emitLine("moveLeft()")
                    #self.moveLeft()
                elif input[positions][0] == 'Stop':
                    self.emitLine("stop()")
                elif input[positions][0] == 'Hammer':
                    orientation = input[positions][2]
                    self.emitLine("hammer("+orientation+")")
                    #self.stop()
                elif input[positions][0] == 'While':
                    self.whileStatement(input[positions])
                elif input[positions][0] == 'Until':
                    self.untilStatement(input[positions])
            elif input[positions] == '(':
                self.identation += 1
            elif input[positions] == ')':
                self.identation -= 1
            else:
                return positions
    
    def isTrue(self, input):
        variableName = self.getVariableName(input, 2, False)
        return variableName

#['AlterB', '(', '@var', ')']
    def alterB(self, input):
        variableName = self.getVariableName(input, 2, False)
        self.emitLine(variableName + ' = ' + 'not ' + variableName)

    def printValues(self, input):
        pass

    def repeat(self, input):
        pass

    def getCondition(self, positionVarible1, positionOperator, positionVarible2, input):
        if input[positionVarible1][0] == '@':
            variableName1 = self.getVariableName(input, positionVarible1, False)
        else:
            variableName1 = input[positionVarible1]
            
        if input[positionVarible2][0] == '@':
            variableName2 = self.getVariableName(input, positionVarible2, False)
        else:
            variableName2 = input[positionVarible2]

        operator = '!=' if input[positionOperator ] == '<>' else input[positionOperator]
        condition = variableName1 + " " + operator + " " + variableName2

        return condition

    def caseWhen(self, input):
        if isinstance(input[2], list):
            self.emitLine("if " + self.isTrue(input[2]) + ":")
            currentPos = 3
        else:
            condition = self.getCondition(3, 4, 5, input)
            self.emitLine("if " + condition + ":")
            currentPos = 7

        currentPos = self.checkIntructions(currentPos + 1, input)
        if currentPos < len(input):
            self.emitLine("else:")
            self.checkIntructions(currentPos + 1, input)

#['Case', '@mellamocarlos', 'When', '1', 'Then', '(', ['MoveRight'], ['MoveLeft'], ')', 'When', '2', 'Then', '(', ['MoveLeft'], ')']
    def caseSwitch(self, input):
        variableName = self.getVariableName(input, 1, False)
        self.emitLine("if "+ variableName + " == " + input[3]+ ":")
        currentPosition = self.checkIntructions(5, input)
        while currentPosition <= len(input):
            if input[currentPosition] == 'Else':
                self.emitLine("else:")
                self.checkIntructions(currentPosition + 1, input)
                break

            self.emitLine("elif " + variableName + " == " + input[currentPosition + 1] + ":")
            currentPosition += 3
            currentPosition = self.checkIntructions(currentPosition, input)

    def emitFuntions(self):
        functions = {
            'moveRight' : self.moveRight,
            'moveLeft' : self.moveLeft,
            'stop' : self.stop,
            'hammer' : self.hammer
            }
        for function  in functions:
            self.identation = 1 
            if function != 'hammer':
                self.emitLine("def " + function + "():")
            else:
                self.emitLine("def " + function + "(orientation):")
            self.emitIdentation()
            functions.get(function)()          

    def hammer(self):
        self.emitLine("pass")
        self.identation = 0 

        # agregar la position 
        pass

    def moveRight(self):
        self.emitLine("pass")
        self.identation = 0
        #return "# MoveRight"

    def moveLeft(self):
        self.emitLine("pass")
        self.identation = 0 
        #return "# MoveLeft"

    def stop(self):
        self.emitLine("pass")
        self.identation = 0
        #return "# Stop"
    
    def printCode(self):
        return self.code
