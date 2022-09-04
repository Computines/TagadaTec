import sys
from turtle import pos

# ['New', '@variable', ',', '(', 'Num', ',', '5', ')']
# ['Alter', '(', '@variable1', ',', 'SUB', ',', '3', ')']
# ['Values', '(', '@variable2', ',', '51', ')']
# ['Until', '(', '[MoveRight]', ')', '@variable3', operador, '@variable4' ]
# ['Case', '@mellamocarlos', 'When', '1', 'Then', '(', 'MoveRight', 'MoveLeft', 'MoveLeft', ')', 'When', '2', 'Then', '(', 'MoveLeft', ')']

class Emitter:

    def __init__(self, path) -> None:
        self.code = ""
        self.path = path
        self.currentToken = None
        self.nextToken = None
        self.localVariables = []
        self.globalVariables = []

    def abort(self, message):
        sys.exit("Error. " + message)

    def emitLine(self, line):
        self.code += line + '\n'

    def emitIdentation(self):
        self.code += "    "

    def writeFile(self):
        with open(self.path, 'w') as file:
            file.write(self.code)

    def newVariable (self, input):
        variableName = self.getLetter(input, 1, True)
        variableValue = self.getLetter(input, 6, False)

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

    def getLetter(self, input, position, isVariable):
        if isVariable :
            return input[position][1:]
        return input[position]

    def alterVariable(self, input):
        operators = {
            'ADD': '+',
            'SUB' : '-',
            'MUL' : '*',
            'DIV' : '/'
        }

        variableName = self.getLetter(input, 2, True)
        operator = operators.get(input[4])

        if self.checkVariableExistance(variableName):
            return variableName + operator + input[6]

    def valuesStatement(self, input):
        variableName = self.getLetter(input, 2, True)

        if self.checkVariableExistance(variableName):
            if isinstance(input[4], list):
                line = variableName + ' ' + '= ' + self.alterVariable(input[4])
            else:
                line = variableName + ' ' + '= ' + input[4]

            self.emitLine(line)

    def untilStatement(self, input):
        variableName = self.getLetter(input, -3, True)

        if self.checkVariableExistance(variableName):
            operatorPosition = -2
            operating2Position = -1
            operator = '!=' if input[operatorPosition ] == '<>' else input[operatorPosition]
            condition = variableName + " " + operator + " " + input[operating2Position]
            self.emitLine('while ' + condition + ':')
        
        initialPosition = 1
        self.checkIntructions(initialPosition, input)

    def whileStatement(self, input):
        if isinstance(input[1], list): #check if it is IsTrue
            pass
        else:
            variableName = self.getLetter(input, 1, True)

            if self.checkVariableExistance(variableName):
                operatorPosition = 2
                operating2Position = 3
                operator = '!=' if input[operatorPosition ] == '<>' else input[operatorPosition]
                condition = variableName + " " + operator + " " + input[operating2Position]

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
                    self.moveRight()
                elif input[positions][0] == 'MoveLeft':
                    self.moveLeft()
                elif input[positions][0] == 'Stop':
                    self.stop()
                else:
                    input[positions][0] 
            elif input[positions] == '(' or input[positions] == ')':
                pass
            else:
                break
    

    def moveRight(self):
        self.emitLine("# MoveRight")
        #return "# MoveRight"

    def moveLeft(self):
        self.emitLine("# MoveLeft")
        #return "# MoveLeft"

    def stop(self):
        self.emitLine("# Stop")
        #return "# Stop"
    
    def printCode(self):
        return self.code
