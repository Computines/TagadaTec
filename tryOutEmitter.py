from emitter import *

def main():
    
    new = ['New', '@variable1', ',', '(', 'Num', ',', '2', ')']
    new2 = ['New', '@variable2', ',', '(', 'Num', ',', '1', ')']
    values = ['Values', '(', '@variable1', ',', ['Alter', '(', '@variable2', ',', 'SUB', ',', '3', ')'], ')']
    until =  ['Until', '(', ['MoveRight'], ['Values', '(', '@variable1', ',', ['Alter', '(', '@variable2', ',', 'SUB', ',', '3', ')'], ')'],')', '@variable1', '==', '5' ]
    whiles =  ['While', '@variable1', '==', '5' , '(', ['Values', '(', '@variable1', ',', ['Alter', '(', '@variable2', ',', 'SUB', ',', '3', ')'], ')'],')',]
    emitter = Emitter("primerStatement.py")

    emitter.newVariable(new)
    emitter.newVariable(new2)
    emitter.valuesStatement(values)
    emitter.untilStatement(until)
    emitter.whileStatement(whiles)
    emitter.writeFile()

main() 