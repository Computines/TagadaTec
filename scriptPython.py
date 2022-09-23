def principal():
    global tryout 
    tryout = 5
    proc()

def proc():
    suma = tryout + 2
    print(suma)
    seg()

def seg():
    suma = tryout - 2
    print(suma)

principal()