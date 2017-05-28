import json
from time import sleep

import falcon
import wiringpi as wiringpi

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


def dc_motor_init(num):
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


def dc_motor_run(motornum, cmd):
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
        latch_state &= ~_BV(a)
        latch_state |= _BV(b)
        latch_tx()

    elif cmd == BACKWARD:
        latch_state |= _BV(a)
        latch_state &= ~_BV(b)
        latch_tx()

    elif cmd == RELEASE:
        latch_state &= ~_BV(a)
        latch_state &= ~_BV(b)
        latch_tx()


def dc_motor_set(motor_num, speed):
    if speed == 0:
        dc_motor_run(motor_num, RELEASE)
    else:
        if speed > 0:
            cmd = FORWARD
        else:
            cmd = BACKWARD

        if motor_num == 1:
            pwm = MOTOR_1_PWM
        elif motor_num == 2:
            pwm = MOTOR_2_PWM
        elif motor_num == 3:
            pwm = MOTOR_3_PWM
        elif motor_num == 4:
            pwm = MOTOR_4_PWM

        dc_motor_run(motor_num, cmd)
        wiringpi.softPwmWrite(pwm, abs(speed))


def initialize_car():
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

    dc_motor_init(1)
    dc_motor_init(2)
    dc_motor_init(3)
    dc_motor_init(4)

    wiringpi.pinMode(LED_FORWARD, OUTPUT)

    print("initialized!")


def test_motors():
    print("motor 1")

    dc_motor_run(1, FORWARD)
    wiringpi.softPwmWrite(MOTOR_1_PWM, 100)
    sleep(1)

    dc_motor_run(1, RELEASE)
    sleep(1)

    dc_motor_run(1, BACKWARD)
    sleep(1)

    dc_motor_run(1, RELEASE)
    sleep(1)

    print("motor 2")

    dc_motor_run(2, FORWARD)
    wiringpi.softPwmWrite(MOTOR_2_PWM, 100)
    sleep(1)

    dc_motor_run(2, RELEASE)
    sleep(1)

    dc_motor_run(2, BACKWARD)
    sleep(1)

    dc_motor_run(2, RELEASE)
    sleep(1)

    print("motor 3")

    dc_motor_run(3, FORWARD)
    wiringpi.softPwmWrite(MOTOR_3_PWM, 100)
    sleep(1)

    dc_motor_run(3, RELEASE)
    sleep(1)

    dc_motor_run(3, BACKWARD)
    sleep(1)

    dc_motor_run(3, RELEASE)
    sleep(1)

    print("motor 4")

    dc_motor_run(4, FORWARD)
    wiringpi.softPwmWrite(MOTOR_4_PWM, 100)
    sleep(1)

    dc_motor_run(4, RELEASE)
    sleep(1)

    dc_motor_run(4, BACKWARD)
    sleep(1)

    dc_motor_run(4, RELEASE)
    sleep(1)


def turn_left():
    dc_motor_set(1, 100)
    dc_motor_set(2, 100)
    dc_motor_set(3, 10)
    dc_motor_set(4, 10)


def turn_right():
    dc_motor_set(1, 10)
    dc_motor_set(2, 10)
    dc_motor_set(3, 100)
    dc_motor_set(4, 100)


def move_forward():
    dc_motor_set(1, 100)
    dc_motor_set(2, 100)
    dc_motor_set(3, 100)
    dc_motor_set(4, 100)


def move_backward():
    dc_motor_set(1, -100)
    dc_motor_set(2, -100)
    dc_motor_set(3, -100)
    dc_motor_set(4, -100)


def move(thrust, vector):
    if (vector == 0):
        thrustl = thrust
        thrustr = thrust
    elif (vector < 0):
        thrustr = thrust
        thrustl = int(float(thrust) * (1.0+vector))
    elif (vector > 0):
        thrustl = thrust
        thrustr = int(float(thrust) * (1.0-vector))

    dc_motor_set(1, thrustr)
    dc_motor_set(2, thrustr)
    dc_motor_set(3, thrustl)
    dc_motor_set(4, thrustl)


def release():
    dc_motor_set(1, 0)
    dc_motor_set(2, 0)
    dc_motor_set(3, 0)
    dc_motor_set(4, 0)


def lights_on():
    wiringpi.digitalWrite(LED_FORWARD, HIGH)


def lights_off():
    wiringpi.digitalWrite(LED_FORWARD, LOW)


class CarMoveForward:
    def on_get(self, req, resp):
        move_forward()
        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)
        resp.body = json.dumps({
            'status': 'forward'
        })
        resp.status = falcon.HTTP_200


class CarTurnLeft:
    def on_get(self, req, resp):
        turn_left()
        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)
        resp.body = json.dumps({
            'status': 'left'
        })
        resp.status = falcon.HTTP_200


class CarTurnRight:
    def on_get(self, req, resp):
        turn_right()
        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)
        resp.body = json.dumps({
            'status': 'right'
        })
        resp.status = falcon.HTTP_200


class CarMoveBackward:
    def on_get(self, req, resp):
        move_backward()
        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)
        resp.body = json.dumps({
            'status': 'backward'
        })
        resp.status = falcon.HTTP_200

class CarMove:
    def on_get(self, req, resp, thrust, vector):
        move(int(thrust), float(vector))
        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)
        resp.body = json.dumps({
            'status': 'move',
            'thrust': thrust,
            'vector': vector
        })
        resp.status = falcon.HTTP_200


class CarRelease:
    def on_get(self, req, resp):
        release()
        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)
        resp.body = json.dumps({
            'status': 'stop'
        })
        resp.status = falcon.HTTP_200


class CarLightsOn:
    def on_get(self, req, resp):
        lights_on()

        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)
        resp.body = json.dumps({
            'status': 'lights_on'
        })
        resp.status = falcon.HTTP_200


class CarLightsOff:
    def on_get(self, req, resp):
        lights_off()

        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)

        resp.body = json.dumps({
            'status': 'lights_off'
        })
        resp.status = falcon.HTTP_200


def start_this_app():
    initialize_car()


start_this_app()

app = falcon.API()

app.add_route('/car/fw', CarMoveForward())
app.add_route('/car/f9/{thrust}/{vector}', CarMove())
app.add_route('/car/tl', CarTurnLeft())
app.add_route('/car/tr', CarTurnRight())
app.add_route('/car/bw', CarMoveBackward())
app.add_route('/car/st', CarRelease())
app.add_route('/car/lightson', CarLightsOn())
app.add_route('/car/lightsoff', CarLightsOff())
