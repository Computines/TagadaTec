
from lex import *
from parser import *
from emitter import *

# def main():
# 	input = "==<="
# 	lexer = Lexer(input)

# 	while lexer.peek() != '\0':
# 		print(lexer.getToken().kind)
# 		lexer.nextChar()

def main():
    # input = "New @pepe, (Num, 5);\n Values(@pepe, Alter(@pepe, SUB, 3));\n Values(@pepe, 51);\n MoveRight;\n Case @mellamocarlos \n When 1 Then \n ( MoveRight;\n MoveLeft;\n ) \n When 2 Then \n ( MoveLeft;\n );"
    #input = "Case @mellamocarlos \n When 1 Then \n ( MoveRight;\n MoveLeft;\n ) \n When 2 Then \n ( MoveLeft;\n );"
    # input = "Proc @trep ( New @variable2,(Num,5);\n New @variable1,(Num,5);\n Values(@variable2, Alter(@variable1, SUB, 3));\n );\n New @pepe, (Num, 4);\n CALL(@trep);\n"
    input = "New @pepe, (Num, 4);\n Values(@pepe, Alter(@pepe, SUB, 7));\n"
    lexer = Lexer(input)
    emitter = Emitter("Trep.py")
    parser = Parser(lexer, emitter)
    #token = lexer.getToken()
    parser.program()
    
    #while token.kind != TokenType.EOF:
    #    print(token.kind)   
    #    token = lexer.getToken()

main()