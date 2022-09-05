from emitter import *

def main():
    
    new = ['New', '@variable1', ',', '(', 'Num', ',', '2', ')']
    new2 = ['New', '@variable2', ',', '(', 'Num', ',', '1', ')']
    new3 = ['New', '@variable3', ',', '(', 'Num', ',', '1', ')']
    new4 = ['New', '@variableBool', ',', '(', 'Bool', ',', 'true', ')']
    new5 = ['New', '@mellamocarlos', ',', '(', 'Num', ',', '1', ')']
    values = ['Values', '(', '@variable1', ',', ['Alter', '(', '@variable2', ',', 'SUB', ',', '3', ')'], ')']
    until =  ['Until', '(', ['MoveRight'], ['While', '@variable1', '==', '5' , '(', ['Values', '(', '@variable1', ',', ['Alter', '(', '@variable2', ',', 'SUB', ',', '3', ')'], ')'],')',],')', '@variable1', '>=', '5' ]
    whiles =  ['While', '@variable1', '==', '5' , '(', ['Values', '(', '@variable1', ',', ['Alter', '(', '@variable2', ',', 'SUB', ',', '3', ')'], ')'],')',]
    whilesTrue =  ['While', ['IsTrue', '(', '@variableBool', ')'], '(', ['Values', '(', '@variable1', ',', ['Alter', '(', '@variable2', ',', 'SUB', ',', '3', ')'], ')'],')',]
    caseWhen = ['Case', 'When', ['IsTrue', '(', '@variableBool', ')'], 'Then', '(', ['MoveRight'], ')', 'Else', '(', ['MoveLeft'], ')']
    caseSwicth = ['Case', '@mellamocarlos', 'When', '1', 'Then', '(', ['MoveRight'], ['MoveLeft'], ')', 'When', '2', 'Then', '(', ['MoveLeft'],')','Else','(', ['MoveRight'], ')']
    alterB = ['AlterB', '(', '@variableBool', ')']

    emitter = Emitter("primerStatement2.py")
    emitter.commonFuntions()
    emitter.newVariable(new)
    emitter.newVariable(new2)
    emitter.newVariable(new3)
    emitter.newVariable(new4)
    emitter.newVariable(new5)
    emitter.valuesStatement(values)
    emitter.untilStatement(until)
    emitter.caseSwitch(caseSwicth)
    emitter.whileStatement(whiles)
    emitter.caseWhen(caseWhen)
    emitter.whileStatement(whilesTrue)
    emitter.alterB(alterB)
    emitter.writeFile()

main() 