from lex import *


# def main():
# 	input = "==<="
# 	lexer = Lexer(input)

# 	while lexer.peek() != '\0':
# 		print(lexer.getToken().kind)
# 		lexer.nextChar()

def main():
    input = "ADD<===<>>Values<PrintValues<Hammer@variable,>741Num>Bool)()"
    lexer = Lexer(input)

    token = lexer.getToken()
    while token.kind != TokenType.EOF:
        print(token.kind)   
        token = lexer.getToken()

main()