from pymata4 import pymata4
import time
numStep = 512
pinStepper = [7,5,6,4]
board = pymata4.Pymata4()
phase1 = -5
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
N = 'N'
S = 'S'
E = 'E'
O = 'O'
def moveRight():
    board.stepper_write(25, 1100)
    time.sleep(7)
def moveLeft():
    board.stepper_write(25, -1100)
    time.sleep(7)
def stop():
    pass
def hammer(orientation):
    if orientation == 'N':
        board.servo_write(8, 115-phase1)
        time.sleep(1)
        board.servo_write(8, 90-phase1)
        time.sleep(1)
    elif orientation == 'S':
        board.servo_write(8, 65-phase1)
        time.sleep(1)
        board.servo_write(8, 90-phase1)
        time.sleep(1)
    elif orientation == 'O':
        board.servo_write(9, 115-phase1)
        time.sleep(1)
        board.servo_write(9, 90-phase1)
        time.sleep(1)
    elif orientation == 'E':
        board.servo_write(9, 65-phase1)
        time.sleep(1)
        board.servo_write(9, 90-phase1)
        time.sleep(1)
def principal():
    global levels
    levels = true
    global control
    control = 0
    while control < 2:
        if levels:
            medium()
            levels = not levels
        else:
            easy()
            hard()
        control = control+1
    pass

def easy():
    control = 0
    while control < 4:
        if control == 1:
            moveRight()
        elif control == 2:
            moveLeft()
        elif control == 3:
            moveRight()
        control = control+1
    
def medium():
    hits = 0
    moveRight()
    hammer(N)
    moveLeft()
    hammer(S)
    hits = hits+1
    while hits < 2:
        moveRight()
        hammer(N)
        moveLeft()
        hammer(S)
        hits = hits+1
    
def hard():
    while True:
        hammer(N)
        hammer(O)
        moveRight()
        hammer(E)
        hammer(S)
        moveLeft()
        break
    
principal()
