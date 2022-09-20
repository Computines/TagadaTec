import sys

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
        self.identation = 0
        self.commonFuntions()

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

    def emitStatement(self, input):
        print("emitStatement")
        print(input)
        if input[0] != 'Until':
            self.emitIdentation()
        if input[0] == 'Proc':
            self.procStatement(input)
        elif input[0] == 'EndProc':
            self.endProc()
        elif input[0] == 'Values':
            print("values")
            self.valuesStatement(input)
        elif input[0] == 'MoveRight':
            self.emitLine("moveRight()")
        elif input[0] == 'MoveLeft':
            self.emitLine("moveLeft()")
        elif input[0] == 'Stop':
            self.emitLine("stop()")
        elif input[0]== 'Hammer':
            orientation = input[2]
            self.emitLine("hammer("+orientation+")")
        elif input[0] == 'While':
            self.whileStatement(input)
        elif input[0] == 'Until':
            self.untilStatement(input)
        elif input[0] == 'New':
            print("new")
            self.newVariable(input)
        elif input[0] == 'Repeat':
            self.repeat(input)
        elif input[0] == 'Case':
            if input[1] == 'When':
                self.caseWhen(input)
            else:
                self.caseSwitch(input)
        elif input[0] == 'PrintValues':
            self.printValues(input)
        elif input[0] == 'AlterB':
            self.alterB(input)
        elif input[0] == 'CALL':
            print("estoy en el call")
            self.callStatement(input)

    def getVariableName(self, input, position):
        variableName = input[position][1:]
        return variableName

#[Proc, @nombreProc]
    def procStatement(self, input):
        procName = self.getVariableName(input, 1)
        self.emitLine('def ' + procName + '():')
        self.identation = 1
    
    def endProc(self):
        self.emitLine("")
        self.identation = 0

    def newVariable (self, input):
        variableName = self.getVariableName(input, 1)
        variableValue = input[6]
        line = variableName + ' = ' + variableValue
        self.emitLine(line)


    def alterVariable(self, input):
        operators = {
            'ADD': '+',
            'SUB' : '-',
            'MUL' : '*',
            'DIV' : '/'
        }

        variableName = self.getVariableName(input, 2)
        operator = operators.get(input[4])

        return variableName + operator + input[6]

    def valuesStatement(self, input):
        variableName = self.getVariableName(input, 2)
        if isinstance(input[4], list):
            line = variableName + ' ' + '= ' + self.alterVariable(input[4])
        else:
            line = variableName + ' ' + '= ' + input[4]

        self.emitLine(line)

    def isTrue(self, input):
        variableName = self.getVariableName(input, 2)
        return variableName

#['AlterB', '(', '@var', ')']
    def alterB(self, input):
        variableName = self.getVariableName(input, 2)
        self.emitLine(variableName + ' = ' + 'not ' + variableName)

#['PrintValues', '(', '"Hola"', ',' , '@variable1',')']
    def printValues(self, input):
        insidePrint = '""'
        for element in input[2:len(input)-1]:
            if element[0] == '@':
                insidePrint = insidePrint + '+'+ "str(" + element[1:] + ")" + '+'+ '" "'
            elif element[0] == '\"':
                insidePrint = insidePrint + '+' + element + '+' +'" "' 
        self.emitLine("print(" + insidePrint + ")")

#until =  ['Until', '(', ['MoveRight'], ['While', '@variable1', '==', '5' , '(', ['Values', '(', '@variable1', ',', ['Alter', '(', '@variable2', ',', 'SUB', ',', '3', ')'], ')'],')',],')', '@variable1', '>=', '5' ]
    def untilStatement(self, input):
        tempIndentation = self.identation
        self.checkIntructions(2, input)
        self.identation = tempIndentation
        condition = self.getCondition(-3, -2, -1, input)
        self.emitIdentation()
        self.emitLine('while ' + condition + ':')
        self.checkIntructions(1, input)
        
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

    def repeat(self, input):
        self.emitLine("while True:")
        self.checkIntructions(1, input)

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
            self.emitIdentation()
            self.emitLine("else:")
            self.checkIntructions(currentPos + 1, input)

#['Case', '@mellamocarlos', 'When', '1', 'Then', '(', ['MoveRight'], ['MoveLeft'], ')', 'When', '2', 'Then', '(', ['MoveLeft'],')','Else','(', ['MoveRight'], ')']
    def caseSwitch(self, input):
        variableName = self.getVariableName(input, 1)
        self.emitLine("if "+ variableName + " == " + input[3]+ ":")
        currentPosition = self.checkIntructions(5, input)
        while currentPosition <= len(input):
            self.emitIdentation()
            if input[currentPosition] == 'Else':
                self.emitLine("else:")
                self.checkIntructions(currentPosition + 1, input)
                break
            
            self.emitLine("elif " + variableName + " == " + input[currentPosition + 1] + ":")
            currentPosition += 3
            currentPosition = self.checkIntructions(currentPosition, input)
#[Call, (, @proc, )]
    def callStatement(self, input):
        print("estoy aqui")
        procName = self.getVariableName(input, 2)
        self.emitLine(procName+"()")

    def getCondition(self, positionVarible1, positionOperator, positionVarible2, input):
        if input[positionVarible1][0] == '@':
            variableName1 = self.getVariableName(input, positionVarible1)
        else:
            variableName1 = input[positionVarible1]
            
        if input[positionVarible2][0] == '@':
            variableName2 = self.getVariableName(input, positionVarible2)
        else:
            variableName2 = input[positionVarible2]

        operator = '!=' if input[positionOperator ] == '<>' else input[positionOperator]
        condition = variableName1 + " " + operator + " " + variableName2

        return condition

    def checkIntructions(self, initialPosition, input):
        for position in range(initialPosition, len(input)):
            if isinstance(input[position], list):
                self.emitIdentation()
                if input[position][0] == 'Values':
                    self.valuesStatement(input[position])
                elif input[position][0] == 'MoveRight':
                    self.moveRightStatement()
                elif input[position][0] == 'MoveLeft':
                    self.moveLeftStatement()
                elif input[position][0] == 'Stop':
                    self.stopStatement()
                elif input[position][0] == 'Hammer':
                    orientation = input[position][2]
                    self.hammerStatement(orientation)
                elif input[position][0] == 'While':
                    self.whileStatement(input[position])
                elif input[position][0] == 'Until':
                    self.untilStatement(input[position])
                elif input[position][0] == 'New':
                    self.newVariable(input[position])
                elif input[position][0] == 'Repeat':
                    self.repeat(input[position])
                elif input[position][0] == 'Case':
                    if input[position][1] == 'When':
                        self.caseWhen(input[position])
                    else:
                        self.caseSwitch(input[position])
                elif input[position][0] == 'PrintValues':
                    self.printValues(input[position])
                elif input[position][0] == 'AlterB':
                    self.alterB(input)
            elif input[position] == '(':
                self.identation += 1
            elif input[position] == ')':
                self.identation -= 1
            elif input[position] == 'Break':
                self.emitIdentation()
                self.emitLine("break")
            else:
                return position
    
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

    def hammerStatement(self, orientation):
        self.emitLine("hammer("+orientation+")")

    def moveRightStatement(self):

        self.emitLine("moveRight()")

    def moveLeftStatement(self):
        self.emitLine("moveLeft()")

    def stopStatement(self):
        self.emitLine("stop()")

    def hammer(self):
        self.emitLine("pass")
        self.identation = 0

    def moveRight(self):
        self.emitLine("pass")
        self.identation = 0 

    def moveLeft(self):
        self.emitLine("pass")
        self.identation = 0

    def stop(self):
        self.emitLine("pass")
        self.identation = 0 
    
    def printCode(self):
        return self.code
