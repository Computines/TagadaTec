from tokenController import TokenType, Token
import regex as rex

informalRegex = 'INITIAL_PARENTESIS [STRING|VARIABLE_NAME] ( COMMA [STRING|VARIABLE_NAME] ) ! FINAL_PARENTESIS'

def regexGenerator(informalRegex):
    listTokens = informalRegex.split(" ")
    finalRegex = ""
    # print(listTokens)
    for token in listTokens:
        if token[0] == "[":
            orList = token[1:-1].split("|")
            orRegex = ""
            for t in orList:
                orRegex += f"({Token.checkTokenType(t, 0).value})"
            finalRegex += orRegex.replace(")(", "|")
        elif token == "(" or token == ")" or token == "?":
            finalRegex += token
        elif token == "*":
            finalRegex += ".*"
        elif token == "!":
            finalRegex += "*"
        else:
            try:
                finalRegex += f"({Token.checkTokenType(token, 0).value})"
            except:
                print("Caracter inválido:", token)
        # print(finalRegex)
    return finalRegex

if __name__ == "__main__":
    finalRegex = regexGenerator(informalRegex)
    print(finalRegex)
    # print(rex.fullmatch(r"{x}".format(x=finalRegex), ""))

