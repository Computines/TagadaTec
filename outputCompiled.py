def principal():
    global var1
    var1 = 1
    global var2
    var2 = 2
    global var3
    var3 = 3
    global var4
    var4 = 4
    global varT
    varT = true
    global varF
    varF = false
    while True:
        global variable1
        variable1 = 5
        moveLeft()
        moveRight()
        break
    moveLeft()
    moveRight()
    variable1 = variable1+1
    while variable1 > 10:
        moveLeft()
        moveRight()
        variable1 = variable1+1
    while varT:
        moveLeft()
        moveRight()
        varT = not varT
    if var1 > 2:
        moveLeft()
        moveRight()
    if varT:
        moveLeft()
        moveRight()
    else:
        moveLeft()
        moveLeft()
    if variable1 == 1:
        moveLeft()
    elif variable1 == 2:
        moveRight()
    elif variable1 == 3:
        moveLeft()
    if varF == true:
        moveLeft()
    else:
        moveRight()
    print(""+ "hola" +" "+str(varF)+" ")
    pass

def proc():
    varF = not varF
    
principal()
