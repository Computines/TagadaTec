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
def varia():
    variable1 = 2
    variable2 = 1
    variable3 = 1
    variableBool = true
    mellamocarlos = 1
    variable1 = variable2-3
    stop()
    while variable1 == 5:
        variable1 = variable2-3
    while variable1 >= 5:
        stop()
        while variable1 == 5:
            variable1 = variable2-3
    if mellamocarlos == 1:
        moveRight()
        moveLeft()
    elif mellamocarlos == 2:
        moveLeft()
    else:
        moveRight()
    while variable1 == 5:
        variable1 = variable2-3
    if variableBool:
        moveRight()
    else:
        moveLeft()
    while variableBool:
        variable1 = variable2-3
        break
    variableBool = not variableBool
    while True:
        meSientoFeliz = 1
        break
    print(""+"Hola"+" "+str(variable1)+" ")
    stop()
    while variable1 == 5:
        variable1 = variable2-3
    while variable1 >= 5:
        stop()
        while variable1 == 5:
            variable1 = variable2-3
    
def varia():
    while variableBool:
        variable1 = variable2-3
        break
    if mellamocarlos == 1:
        moveRight()
        moveLeft()
    elif mellamocarlos == 2:
        moveLeft()
    else:
        moveRight()
    stop()
    while variable1 == 5:
        variable1 = variable2-3
    while variable1 >= 5:
        stop()
        while variable1 == 5:
            variable1 = variable2-3
    
