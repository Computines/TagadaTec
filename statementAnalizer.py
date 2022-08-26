from tkinter import S
from tokenize import Token
from typing import List
import regex as rex
from tokenController import Token
from regexGenerator import regexGenerator


class StatementAnalizer():
    
    RegexDictionary = {
        "New" : regexGenerator('New VARIABLE_NAME COMMA INITIAL_PARENTESIS [Num|Bool] COMMA [Number|True|False|Alter] FINAL_PARENTESIS')
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



