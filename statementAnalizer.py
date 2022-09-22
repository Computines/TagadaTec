from traceback import print_tb
from typing import List
import regex as rex
from tokenController import Token
from regexGenerator import regexGenerator


class StatementAnalizer():
    
    RegexDictionary = {
        "New" : regexGenerator('New VARIABLE_NAME COMMA INITIAL_PARENTESIS [Num|Bool] COMMA [Number|true|false|Alter] FINAL_PARENTESIS'),
        "Values" : regexGenerator('Values INITIAL_PARENTESIS VARIABLE_NAME COMMA [Number|true|false|Alter] FINAL_PARENTESIS'),
        "Alter" : regexGenerator('Alter INITIAL_PARENTESIS VARIABLE_NAME COMMA [ADD|SUB|MUL|DIV] COMMA Number FINAL_PARENTESIS'),
        "AlterB" : regexGenerator('AlterB INITIAL_PARENTESIS VARIABLE_NAME FINAL_PARENTESIS'),
        "MoveRight" : regexGenerator('MoveRight'),
        "MoveLeft" : regexGenerator('MoveLeft'),
        "Hammer" : regexGenerator('Hammer INITIAL_PARENTESIS [N|S|O|E] FINAL_PARENTESIS'),
        "Stop" : regexGenerator('Stop'),
        "IsTrue": regexGenerator('IsTrue INITIAL_PARENTESIS VARIABLE_NAME FINAL_PARENTESIS'),
        "PrintValues" : regexGenerator('PrintValues INITIAL_PARENTESIS [STRING|VARIABLE_NAME] ( COMMA [STRING|VARIABLE_NAME] ) ! FINAL_PARENTESIS'),
        "Proc": regexGenerator('Proc VARIABLE_NAME INITIAL_PARENTESIS * FINAL_PARENTESIS'),
        "CALL": regexGenerator('CALL INITIAL_PARENTESIS VARIABLE_NAME FINAL_PARENTESIS'),
        "Repeat": regexGenerator('Repeat INITIAL_PARENTESIS * Break * FINAL_PARENTESIS'),
        "Until": regexGenerator('Until INITIAL_PARENTESIS * FINAL_PARENTESIS VARIABLE_NAME [EQUAL_EQUAL|NOT_EQUAL|LESS|LESS_EQUAL|GREATER|GREATER_EQUAL] [Number|true|false]'),
        "While": regexGenerator('While ( VARIABLE_NAME [EQUAL_EQUAL|NOT_EQUAL|LESS|LESS_EQUAL|GREATER|GREATER_EQUAL] [Number|true|false] | IsTrue ) INITIAL_PARENTESIS * FINAL_PARENTESIS'),
        "Case When": regexGenerator('Case When ( INITIAL_PARENTESIS VARIABLE_NAME [EQUAL_EQUAL|NOT_EQUAL|LESS|LESS_EQUAL|GREATER|GREATER_EQUAL] [Number|true|false] FINAL_PARENTESIS | IsTrue ) Then INITIAL_PARENTESIS * FINAL_PARENTESIS ( Else INITIAL_PARENTESIS * FINAL_PARENTESIS ) ?'),
        "Case": regexGenerator('Case VARIABLE_NAME When [true|false|Number] Then INITIAL_PARENTESIS * FINAL_PARENTESIS ( When [true|false|Number] Then INITIAL_PARENTESIS * FINAL_PARENTESIS ) ! ( Else INITIAL_PARENTESIS * FINAL_PARENTESIS ) ?'),
        "Break": regexGenerator('Break')
    }
    def __init__(self) -> None:
        pass

    @staticmethod
    def listToRegexExpresion(listTokenType: List[Token]) -> str:
        expectedRegex = ""
        for token in listTokenType:
            if isinstance(token, list):
                expectedRegex += f"{token[0].kind.value}"
                # print(token[0].text, end=" ")
            else:
                # print(token.text, end=" ")
                expectedRegex += f"{token.kind.value}"
        # print(expectedRegex)
        return expectedRegex

    @staticmethod
    def analize(listTokenType: List[Token]) -> bool:
        # print(listTokenType[0].text)
        stmt = StatementAnalizer.listToRegexExpresion(listTokenType)
        dictKey = listTokenType[0].text
        # print("regex to analize: ", stmt)
        if dictKey == "Case" and listTokenType[1].text == "When":
            dictKey = "Case When"

        if rex.fullmatch(r'{x}'.format(x=StatementAnalizer.RegexDictionary[dictKey]), \
            stmt) != None:
            return True # The string coincident with the regex
        else:
            return False

if __name__ == "__main__":
    pass
