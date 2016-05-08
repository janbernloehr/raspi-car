#!/usr/bin/python

from time import sleep
import curses

import wiringpi2 as wiringpi

import web

import cv2
import thread

def _BV(bit):
    return 1 << (bit)


MOTORLATCH = 25
MOTORCLK = 22  # 22
MOTORENABLE = 23  # 23
MOTORDATA = 24  # 24
MOTOR_1_PWM = 1  # 18
MOTOR_2_PWM = 27  # 18
MOTOR_3_PWM = 28  # 18
MOTOR_4_PWM = 29  # 18

LED_FORWARD = 26

MOTOR1_A = 2
MOTOR1_B = 3
MOTOR2_A = 1
MOTOR2_B = 4
MOTOR4_A = 0
MOTOR4_B = 6
MOTOR3_A = 5
MOTOR3_B = 7

FORWARD = 1
BACKWARD = 2
BRAKE = 3
RELEASE = 4

INPUT = 0
OUTPUT = 1
PWM_OUTPUT = 2
GPIO_CLOCK = 3
SOFT_PWM_OUTPUT = 4
SOFT_TONE_OUTPUT = 5
PWM_TONE_OUTPUT = 6

LOW = 0
HIGH = 1

latch_state = 0


def latch_tx():
    wiringpi.digitalWrite(MOTORLATCH, LOW)

    wiringpi.digitalWrite(MOTORDATA, LOW)

    for i in range(0, 8):
        wiringpi.digitalWrite(MOTORCLK, LOW)

        if latch_state & _BV(7 - i):
            wiringpi.digitalWrite(MOTORDATA, HIGH)
        else:
            wiringpi.digitalWrite(MOTORDATA, LOW)

        wiringpi.digitalWrite(MOTORCLK, HIGH)

    wiringpi.digitalWrite(MOTORLATCH, HIGH)


def enable():
    global latch_state

    wiringpi.pinMode(MOTORLATCH, OUTPUT)
    wiringpi.pinMode(MOTORENABLE, OUTPUT)
    wiringpi.pinMode(MOTORDATA, OUTPUT)
    wiringpi.pinMode(MOTORCLK, OUTPUT)

    latch_state = 0

    latch_tx()

    wiringpi.digitalWrite(MOTORENABLE, LOW)


def DCMotorInit(num):
    global latch_state

    if num == 1:
        latch_state = latch_state & ~_BV(MOTOR1_A) & ~_BV(MOTOR1_B)
        latch_tx()
    elif num == 2:
        latch_state = latch_state & ~_BV(MOTOR2_A) & ~_BV(MOTOR2_B)
        latch_tx()
    elif num == 3:
        latch_state = latch_state & ~_BV(MOTOR3_A) & ~_BV(MOTOR3_B)
        latch_tx()
    elif num == 4:
        latch_state = latch_state & ~_BV(MOTOR4_A) & ~_BV(MOTOR4_B)
        latch_tx()


def DCMotorRun(motornum, cmd):
    global latch_state

    if motornum == 1:
        a = MOTOR1_A
        b = MOTOR1_B
    elif motornum == 2:
        a = MOTOR2_A
        b = MOTOR2_B
    elif motornum == 3:
        a = MOTOR3_A
        b = MOTOR3_B
    elif motornum == 4:
        a = MOTOR4_A
        b = MOTOR4_B

    if cmd == FORWARD:
        latch_state |= _BV(a)
        latch_state &= ~_BV(b)
        latch_tx()

    elif cmd == BACKWARD:
        latch_state &= ~_BV(a)
        latch_state |= _BV(b)
        latch_tx()

    elif cmd == RELEASE:
        latch_state &= ~_BV(a)
        latch_state &= ~_BV(b)
        latch_tx()


def testMotors():
    print("motor 1")

    DCMotorRun(1, FORWARD)
    wiringpi.softPwmWrite(MOTOR_1_PWM, 100)
    sleep(1)

    DCMotorRun(1, RELEASE)
    sleep(1)

    DCMotorRun(1, BACKWARD)
    sleep(1)

    DCMotorRun(1, RELEASE)
    sleep(1)

    print("motor 2")

    DCMotorRun(2, FORWARD)
    wiringpi.softPwmWrite(MOTOR_2_PWM, 100)
    sleep(1)

    DCMotorRun(2, RELEASE)
    sleep(1)

    DCMotorRun(2, BACKWARD)
    sleep(1)

    DCMotorRun(2, RELEASE)
    sleep(1)

    print("motor 3")

    DCMotorRun(3, FORWARD)
    wiringpi.softPwmWrite(MOTOR_3_PWM, 100)
    sleep(1)

    DCMotorRun(3, RELEASE)
    sleep(1)

    DCMotorRun(3, BACKWARD)
    sleep(1)

    DCMotorRun(3, RELEASE)
    sleep(1)

    print("motor 4")

    DCMotorRun(4, FORWARD)
    wiringpi.softPwmWrite(MOTOR_4_PWM, 100)
    sleep(1)

    DCMotorRun(4, RELEASE)
    sleep(1)

    DCMotorRun(4, BACKWARD)
    sleep(1)

    DCMotorRun(4, RELEASE)
    sleep(1)


def TurnLeft():
    DCMotorRun(1, FORWARD)
    wiringpi.softPwmWrite(MOTOR_1_PWM, 10)

    DCMotorRun(2, FORWARD)
    wiringpi.softPwmWrite(MOTOR_2_PWM, 10)

    DCMotorRun(3, FORWARD)
    wiringpi.softPwmWrite(MOTOR_3_PWM, 100)

    DCMotorRun(4, FORWARD)
    wiringpi.softPwmWrite(MOTOR_4_PWM, 100)


def TurnRight():
    DCMotorRun(1, FORWARD)
    wiringpi.softPwmWrite(MOTOR_1_PWM, 100)

    DCMotorRun(2, FORWARD)
    wiringpi.softPwmWrite(MOTOR_2_PWM, 100)

    DCMotorRun(3, FORWARD)
    wiringpi.softPwmWrite(MOTOR_3_PWM, 10)

    DCMotorRun(4, FORWARD)
    wiringpi.softPwmWrite(MOTOR_4_PWM, 10)


def Straightforward():
    DCMotorRun(1, FORWARD)
    wiringpi.softPwmWrite(MOTOR_1_PWM, 100)

    DCMotorRun(2, FORWARD)
    wiringpi.softPwmWrite(MOTOR_2_PWM, 100)

    DCMotorRun(3, FORWARD)
    wiringpi.softPwmWrite(MOTOR_3_PWM, 100)

    DCMotorRun(4, FORWARD)
    wiringpi.softPwmWrite(MOTOR_4_PWM, 100)


def Backwards():
    DCMotorRun(1, BACKWARD)
    wiringpi.softPwmWrite(MOTOR_1_PWM, 100)

    DCMotorRun(2, BACKWARD)
    wiringpi.softPwmWrite(MOTOR_2_PWM, 100)

    DCMotorRun(3, BACKWARD)
    wiringpi.softPwmWrite(MOTOR_3_PWM, 100)

    DCMotorRun(4, BACKWARD)
    wiringpi.softPwmWrite(MOTOR_4_PWM, 100)


def BreakIt():
    DCMotorRun(1, RELEASE)
    DCMotorRun(2, RELEASE)
    DCMotorRun(3, RELEASE)
    DCMotorRun(4, RELEASE)


def LightsOn():
    wiringpi.digitalWrite(LED_FORWARD, HIGH)

def LightsOff():
    wiringpi.digitalWrite(LED_FORWARD, LOW)


def CaptureImage():
    cap = cv2.VideoCapture(0)  #ignore the errors
    cap.set(3, 640)        #Set the width important because the default will timeout
                       #ignore the error or false response
    cap.set(4, 480)        #Set the height ignore the errors
    r, frame = cap.read()
    cv2.imwrite("/home/pi/webstuff/test.jpg", frame)


def CaptureImages():
    while True:
        CaptureImage()

        sleep(0.25)


def initializeCar():
    print("initializing")

    wiringpi.wiringPiSetup()

    wiringpi.pinMode(MOTOR_1_PWM, OUTPUT)
    wiringpi.pinMode(MOTOR_2_PWM, OUTPUT)
    wiringpi.pinMode(MOTOR_3_PWM, OUTPUT)
    wiringpi.pinMode(MOTOR_4_PWM, OUTPUT)

    wiringpi.softPwmCreate(MOTOR_1_PWM, 0, 100)
    wiringpi.softPwmCreate(MOTOR_2_PWM, 0, 100)
    wiringpi.softPwmCreate(MOTOR_3_PWM, 0, 100)
    wiringpi.softPwmCreate(MOTOR_4_PWM, 0, 100)

    enable()

    DCMotorInit(1)
    DCMotorInit(2)
    DCMotorInit(3)
    DCMotorInit(4)

    wiringpi.pinMode(LED_FORWARD, OUTPUT)

    print("initialized!")

urls = (
    '/car/fw', 'car_forward',
    '/car/tl', 'car_turn_left',
    '/car/tr', 'car_turn_right',
    '/car/bw', 'car_backward',
    '/car/st', 'car_stop',
    '/car/lightson', 'car_lights_on',
    '/car/lightsoff', 'car_lights_off'
)

class car_forward:
    def GET(self):
        Straightforward()
        return "forward"

class car_turn_left:
    def GET(self):
        TurnLeft()
        return "left"

class car_turn_right:
    def GET(self):
        TurnRight()
        return "right"

class car_backward:
    def GET(self):
        Backwards()
        return "backwards"

class car_stop:
    def GET(self):
        BreakIt()
        return "stop"

class car_lights_on:
    def GET(self):
        LightsOn()
        return "lights_on"

class car_lights_off:
    def GET(self):
        LightsOff()
        return "lights_off"

class MyApplication(web.application):
    def run(self, port=8080, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

def startThisApp():
    initializeCar()

    #thread.start_new_thread( CaptureImages, () )

    app = MyApplication(urls, globals())

    app.run(port=8087)

    print("all done")

    return

    # testMotors()

    pressed_key = -1
    last_key = -1
    continue_this = True
    repeat = 0

    stdscr = curses.initscr()

    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    stdscr.timeout(100)

    sleep(1)

    while continue_this:
        pressed_key = stdscr.getch()

        #print("The pressed key is {0} / {1}".format(pressed_key, repeat))

        if last_key != pressed_key:
            repeat = 0

            if pressed_key == ord('w'):
                print("forward")
                Straightforward()
            elif pressed_key == ord('a'):
                print("left")
                TurnLeft()
            elif pressed_key == ord('d'):
                print("right")
                TurnRight()
            elif pressed_key == ord('s'):
                print("backward")
                Backwards()
            elif pressed_key == -1:
                print("no stop")
            elif pressed_key == ord(' '):
                print("stop")
                BreakIt()
            elif pressed_key == ord('x'):
                print("exit")
                continue_this = False
        else:
            repeat += 1

            if pressed_key == -1 and repeat > 1:
                BreakIt()

        last_key = pressed_key

    curses.nocbreak(); stdscr.keypad(0); curses.echo()

    curses.endwin()


if __name__ == '__main__':
    startThisApp()
