from typing import List
import regex as rex
from tokenController import Token
from regexGenerator import regexGenerator


class StatementAnalizer():
    
    RegexDictionary = {
        "New" : regexGenerator('New VARIABLE_NAME COMMA INITIAL_PARENTESIS [Num|Bool] COMMA [Number|True|False|Alter] FINAL_PARENTESIS'),
        "Values" : regexGenerator('Values INITIAL_PARENTESIS VARIABLE_NAME COMMA [Number|True|False|Alter] FINAL_PARENTESIS'),
        "Alter" : regexGenerator('Alter INITIAL_PARENTESIS VARIABLE_NAME COMMA [ADD|SUB|MUL|DIV] COMMA Number FINAL_PARENTESIS'),
        "AlterB" : regexGenerator('AlterB INITIAL_PARENTESIS VARIABLE_NAME FINAL_PARENTESIS'),
        "MoveRight" : regexGenerator('MoveRight'),
        "MoveLeft" : regexGenerator('MoveLeft'),
        "Hammer" : regexGenerator('Hammer INITIAL_PARENTESIS [N|S|O|E] FINAL_PARENTESIS'),
        "Stop" : regexGenerator('Stop'),
        "IsTrue": regexGenerator('IsTrue INITIAL_PARENTESIS VARIABLE_NAME FINAL_PARENTESIS'),
        "PrintValues" : regexGenerator('INITIAL_PARENTESIS [STRING|VARIABLE_NAME] FINAL_PARENTESIS')
    } 

    def __init__(self) -> None:
        pass

    @staticmethod
    def listToRegexExpresion(listTokenType: List[Token]) -> str:
        expectedRegex = ""
        for token in listTokenType:
            expectedRegex += f"{token.kind.value}"
        # print(expectedRegex)
        return expectedRegex


    @staticmethod
    def analize(listTokenType: List[Token]) -> bool:
        if rex.fullmatch(r'{x}'.format(x=StatementAnalizer.RegexDictionary[listTokenType[0].text]), \
            StatementAnalizer.listToRegexExpresion(listTokenType)) != None:
            return True
        else:
            return False

if __name__ == "__main__":


