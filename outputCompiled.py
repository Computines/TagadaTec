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
def trep():
    variable2 = 5
    variable1 = 5
    fium = 2
    variable2 = fium-3
    print(""+str(variable2)+" ")
    
def proc():
    variable2 = 3
    variable1 = 5
    trululu = 5
    variable2 = trululu+3
    
def principal():
    global bool
    bool = true
    global trululu
    trululu = 3
    global fium
    fium = 5
    trululu = fium+3
    trep()
    proc()
    pass

principal()
