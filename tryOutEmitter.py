from emitter import *

def main():
    
    new = ['New', '@variable1', ',', '(', 'Num', ',', '2', ')']
    new2 = ['New', '@variable2', ',', '(', 'Num', ',', '1', ')']
    values = ['Values', '(', '@variable1', ',', ['Alter', '(', '@variable2', ',', 'SUB', ',', '3', ')'], ')']

    emitter = Emitter("primerStatement.py")

    emitter.newVariable(new)
    emitter.newVariable(new2)
    emitter.valuesStatement(values)
    emitter.writeFile()

main() 