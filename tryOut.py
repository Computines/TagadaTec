
from lex import *
from parser import *

# def main():
# 	input = "==<="
# 	lexer = Lexer(input)

# 	while lexer.peek() != '\0':
# 		print(lexer.getToken().kind)
# 		lexer.nextChar()

def main():
    # input = "New @pepe, (Num, 5);\n Values(@pepe, Alter(@pepe, SUB, 3));\n Values(@pepe, 51);\n MoveRight;\n Case @mellamocarlos \n When 1 Then \n ( MoveRight;\n MoveLeft;\n ) \n When 2 Then \n ( MoveLeft;\n );"
    # input = "Case @mellamocarlos \n When 1 Then \n ( MoveRight;\n MoveLeft;\n ) \n When 2 Then \n ( MoveLeft;\n );"
    # input = "Proc @trep (\n\nValues(@variable2, Alter(@variable1, SUB, 3));\n);"
    input = "New @pepe, (Num, 4);\n Values(@pepe, Alter(@pepe, SUB, 3));\n AlterB(@pepe);\n"
    lexer = Lexer(input)
    #parser = Parser(lexer)
    token = lexer.getToken()
    #parser.program()

    while token.kind != TokenType.EOF:
        print(token.kind)   
        token = lexer.getToken()

main()