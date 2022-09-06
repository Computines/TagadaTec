from email.message import EmailMessage
from timeit import repeat
from emitter import *

def main():
    
    new = ['New', '@variable1', ',', '(', 'Num', ',', '2', ')']
    new2 = ['New', '@variable2', ',', '(', 'Num', ',', '1', ')']
    new3 = ['New', '@variable3', ',', '(', 'Num', ',', '1', ')']
    new4 = ['New', '@variableBool', ',', '(', 'Bool', ',', 'true', ')']
    new5 = ['New', '@mellamocarlos', ',', '(', 'Num', ',', '1', ')']
    new6 = ['New', '@meSientoFeliz', ',', '(', 'Num', ',', '1', ')']
    values = ['Values', '(', '@variable1', ',', ['Alter', '(', '@variable2', ',', 'SUB', ',', '3', ')'], ')']
    until =  ['Until', '(', ['MoveRight'], ['While', '@variable1', '==', '5' , '(', ['Values', '(', '@variable1', ',', ['Alter', '(', '@variable2', ',', 'SUB', ',', '3', ')'], ')'],')',],')', '@variable1', '>=', '5' ]
    whiles =  ['While', '@variable1', '==', '5' , '(', ['Values', '(', '@variable1', ',', ['Alter', '(', '@variable2', ',', 'SUB', ',', '3', ')'], ')'],')',]
    whilesTrue =  ['While', ['IsTrue', '(', '@variableBool', ')'], '(', ['Values', '(', '@variable1', ',', ['Alter', '(', '@variable2', ',', 'SUB', ',', '3', ')'], ')'], 'Break',')',]
    caseWhen = ['Case', 'When', ['IsTrue', '(', '@variableBool', ')'], 'Then', '(', ['MoveRight'], ')', 'Else', '(', ['MoveLeft'], ')']
    caseSwicth = ['Case', '@mellamocarlos', 'When', '1', 'Then', '(', ['MoveRight'], ['MoveLeft'], ')', 'When', '2', 'Then', '(', ['MoveLeft'],')','Else','(', ['MoveRight'], ')']
    alterB = ['AlterB', '(', '@variableBool', ')']
    repeat = ['Repeat', '(', ['New', '@meSientoFeliz', ',', '(', 'Num', ',', '1', ')'], 'Break' , ')']
    printV = ['PrintValues', '(', '"Hola"', ',' , '@variable1',')']

    emitter = Emitter("computines.py")
    emitter.emitStatement(new)
    emitter.emitStatement(new2)
    emitter.emitStatement(new3)
    emitter.emitStatement(new4)
    emitter.emitStatement(new5)
    emitter.emitStatement(values)
    emitter.emitStatement(until)
    emitter.emitStatement(caseSwicth)
    emitter.emitStatement(whiles)
    emitter.emitStatement(caseWhen)
    emitter.emitStatement(whilesTrue)
    emitter.emitStatement(alterB)
    emitter.emitStatement(repeat)
    emitter.emitStatement(printV)
    
    emitter.writeFile()

main() 