
# New nombre_variable, (tipodato, valor);

"""
nombre_variable = valor
"""

# Values (nombre_variable, valor);

"""
nombre_variable = valor
"""

# Alter (nombre_variable, operador, valor);

"""
def Alter (nombre_variable, operador, valor):

    if operador == ADD:
        nombre_variable += valor
    elif operador == SUB:
        nombre_variable -= valor
    elif operador == MUL:
        nombre_variable *= valor
    elif operador == DIV:
        if valor =! 0:
            nombre_variable /= valor
        else:
            return "Invalid operation"
    else:
        return "Invalid operator"

    return nombre_variable
"""

# AlterB (nombre_variable);

"""
def AlterB (nombre_variable):
    if nombre_variable:
        nombre_variable = False
    else:
        nombre_variable = True
"""

# IsTrue (nombre_variable);

"""
def IsTrue (nombre_variable):
    if type(nombre_varibale) == bool:
        return nombre variable
    else:
        return "Error, variable not boolean"
"""

# Repeat (instrucciones);

"""
while True:
    instrucciones
"""

# Until (instrucciones) condicion;

"""
def Until (instrucciones, condicion):
    while condicion:
        instrucciones
"""

# While condicion (instrucciones);

"""
wtf
"""

# Case When (condicion) Then (instrucciones) Else (instrucciones2);

"""
if condicion:
    instrucciones

else:
    instrucciones2
"""

# Case nombre_variable When valor1 Then (instrucciones) When valor2 Then (instrucciones2) When valor3 Then (instrucciones3) Else (instrucciones4);

"""
if nombre_variable == valor1:
    instrucciones

elif nombre_variable == valor2:
    instrucciones2

elif nombre_variable == valor3:
    instrucciones3

else:
    instrucciones4
"""

# PrintValues (valor);

"""
def PrintValues (valor):

    printInConsole(valor)
"""