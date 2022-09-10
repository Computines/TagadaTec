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
        #"PrintValues" : regexGenerator('INITIAL_PARENTESIS [STRING|VARIABLE_NAME] (COMMA [STRING|VARIABLE_NAME])! FINAL_PARENTESIS'),
        #"Proc": regexGenerator('Proc VARIABLE_NAME INITIAL_PARENTESIS * FINALPARENTESIS'),
        "CALL": regexGenerator('CALL INITIAL_PARENTESIS VARIABLE_NAME FINAL_PARENTESIS'),
        "Repeat": regexGenerator('Repeat INITIAL_PARENTESIS * FINAL_PARENTESIS'),
        "Until": regexGenerator('Until INITIAL_PARENTESIS * FINAL_PARENTESIS [Number|true|false|VARIABLE_NAME] [EQUAL_EQUAL|NOT_EQUAL|LESS|LESS_EQUAL|GREATER|GREATER_EQUAL] [Number|true|false|VARIABLE_NAME]'),
        "While": regexGenerator('While [Number|true|false|VARIABLE_NAME] [EQUAL_EQUAL|NOT_EQUAL|LESS|LESS_EQUAL|GREATER|GREATER_EQUAL] [Number|true|false|VARIABLE_NAME] INITIAL_PARENTESIS * FINAL_PARENTESIS')
        #"Case When": regexGenerator('Case When INITIAL_PARENTESIS [Number|true|false|VARIABLE_NAME] [EQUAL_EQUAL|NOT_EQUAL|LESS|LESS_EQUAL|GREATER|GREATER_EQUAL] [Number|true|false|VARIABLE_NAME] FINAL_PARENTESIS Then INITIAL_PARENTESIS * FINAL_PARENTESIS [Else INITIAL_PARENTEISIS * FINAL_PARENTESIS|]'),
        #"Case": regexGenerator('Case VARIABLE_NAME When [true|false|Number] Then INITIAL_PARENTESIS * FINAL_PARENTESIS (When [true|false|Number] Then INITIAL_PARENTESIS * FINAL_PARENTESIS)! [Else INITIAL_PARENTESIS * FINAL_PARENTESIS|]'),
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
    pass
