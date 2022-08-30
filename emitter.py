import sys

# ['New', '@variable', ',', '(', 'Num', ',', '5', ')']
# ['Alter', '(', '@variable1', ',', 'SUB', ',', '3', ')']
# ['Values', '(', '@variable2', ',', '51', ')']

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

    def newVariable (self, input):
        variableName = self.getLetter(input, 1, True)
        variableValue = self.getLetter(input, 6, False)

        if variableName not in self.globalVariables:
            self.globalVariables.append(variableName)
            self.emitLine(variableName + ' = ' + variableValue)
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
                self.emitLine(variableName + ' ' + '= ' + self.alterVariable(input[4]))
            else:
                self.emitLine(variableName + ' ' + '= ' + input[4])


    def printCode(self):
        return self.code
