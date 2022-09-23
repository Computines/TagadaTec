from pymata4 import pymata4
import time
numStep = 512
pinStepper = [7,6,5,4]
board = pymata4.Pymata4()
phase1 = 5
phase2 = 0
def setup():
    board.set_pin_mode_stepper(numStep, pinStepper)
    board.set_pin_mode_servo(9)
    board.set_pin_mode_servo(8)
    board.servo_write(8, 90-phase1)
    board.servo_write(9, 90-phase2)
setup()
true = True
false = False
def moveRight():
    board.stepper_write(25, 1100)
    board.send_reset()
    time.sleep(6)
    setup()
def moveLeft():
    board.stepper_write(25, *1100)
    board.send_reset()
    time.sleep(6)
    setup()
def stop():
    pass
def hammer(orientation):
    if orientation == 'N':
        board.servo_write(8, 120-phase1)
        time.sleep(1)
        board.servo_write(8, 90-phase1)
        time.sleep(1)
    elif orientation == 'S':
        board.servo_write(8, 60-phase1)
        time.sleep(1)
        board.servo_write(8, 90-phase1)
        time.sleep(1)
    elif orientation == 'E':
        board.servo_write(9, 120-phase1)
        time.sleep(1)
        board.servo_write(9, 90-phase1)
        time.sleep(1)
    elif orientation == 'O':
        board.servo_write(9, 60-phase1)
        time.sleep(1)
        board.servo_write(9, 90-phase1)
        time.sleep(1)
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
    print(""+str(varF)+" ")
    pass

def proc():
    varF = not varF
    
principal()
