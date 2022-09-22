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
    pass
Filetoex = 5
