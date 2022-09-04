from tokenController import TokenType, Token
import regex as rex

informalRegex = 'New VARIABLE_NAME COMMA INITIAL_PARENTESIS [Num|Bool] COMMA [Number|True|False|Alter] FINAL_PARENTESIS'

def regexGenerator(informalRegex):
    listTokens = informalRegex.split(" ")
    finalRegex = ""
    for token in listTokens:
        if token[0] == "[":
            orList = token[1:-1].split("|")
            orRegex = ""
            for t in orList:
                orRegex += f"({Token.checkTokenType(t, 0).value})"
            finalRegex += orRegex.replace(")(", "|")
        elif token == "*":
            finalRegex += ".*"
        else:
            finalRegex += f"({Token.checkTokenType(token, 0).value})"
        # print(finalRegex)
    return finalRegex

if __name__ == "__main__":
    finalRegex = regexGenerator(informalRegex)
    print(finalRegex)
    # print(rex.fullmatch(r"{x}".format(x=finalRegex), ""))

