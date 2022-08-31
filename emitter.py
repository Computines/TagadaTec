import sys
from turtle import pos

# ['New', '@variable', ',', '(', 'Num', ',', '5', ')']
# ['Alter', '(', '@variable1', ',', 'SUB', ',', '3', ')']
# ['Values', '(', '@variable2', ',', '51', ')']
# ['Until', '(', '[MoveRight]', ')', '@variable3', operador, '@variable4' ]

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

    def writeFile(self):
        with open(self.path, 'w') as file:
            file.write(self.code)

    def newVariable (self, input, emitLineFlag):
        variableName = self.getLetter(input, 1, True)
        variableValue = self.getLetter(input, 6, False)

        if variableName not in self.globalVariables:
            self.globalVariables.append(variableName)
            line = variableName + ' = ' + variableValue
            if emitLineFlag:
                self.emitLine(line)
            else:
                return line
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

    def valuesStatement(self, input, emitLineFlag):
        variableName = self.getLetter(input, 2, True)

        if self.checkVariableExistance(variableName):
            if isinstance(input[4], list):
                line = variableName + ' ' + '= ' + self.alterVariable(input[4])
            else:
                line = variableName + ' ' + '= ' + input[4]
            
            if emitLineFlag:
                self.emitLine(line)
            else:
                return line


    def untilStatement(self, input):
        operating1Position = 0 
        
        instructions = "instructions"

        for positions in range(1, len(input) + 1 ):
            if isinstance(input[positions], list):
                if input[positions][0] == 'Values':
                    instructions = instructions + '\n' + self.valuesStatement(input[positions], False) 
                else:
                    instructions = instructions + '\n' + input[positions][0] 
            elif input[positions] == '(' or input[positions] == ')':
                pass
            else:
                operating1Position = positions
                break
        
        variableName = self.getLetter(input, operating1Position, True)

        if self.checkVariableExistance(variableName):
            operatorPosition = operating1Position + 1
            operating2Position = operating1Position + 2
            operator = '!=' if input[operatorPosition ] == '<>' else input[operatorPosition]
            condition = variableName +  operator + input[operating2Position]
            self.emitLine('while ' + condition + ':' + '\n' + instructions)

    def whileStatement(self, input):

        instructions = "instructions"

        if isinstance(input[1], list):
            pass
        else:
            variableName = self.getLetter(input, 1, True)

            if self.checkVariableExistance(variableName):
                operatorPosition = 2
                operating2Position = 3
                operator = '!=' if input[operatorPosition ] == '<>' else input[operatorPosition]
                condition = variableName +  operator + input[operating2Position]

            for positions in range(4, len(input)):
                if isinstance(input[positions], list):
                    if input[positions][0] == 'Values':
                        instructions = instructions + '\n' +  self.valuesStatement(input[positions], False)
                    else:
                        instructions = instructions + '\n' + input[positions][0] 
                elif input[positions] == '(' or input[positions] == ')':
                    pass
        
            self.emitLine('while ' + condition + ':' + '\n' + instructions)           

    
    def printCode(self):
        return self.code
