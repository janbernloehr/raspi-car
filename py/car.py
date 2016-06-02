import json
from time import sleep
import falcon

class CarMoveForward:
    def on_get(self, req, resp):
        #move_forward()
        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)
        resp.body = json.dumps({
            'status': 'forward'
        })
        resp.status = falcon.HTTP_200


class CarTurnLeft:
    def on_get(self, req, resp):
        #turn_left()
        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)
        resp.body = json.dumps({
            'status': 'left'
        })
        resp.status = falcon.HTTP_200


class CarTurnRight:
    def on_get(self, req, resp):
        #turn_right()
        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)
        resp.body = json.dumps({
            'status': 'right'
        })
        resp.status = falcon.HTTP_200


class CarMoveBackward:
    def on_get(self, req, resp):
        #move_backward()
        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)
        resp.body = json.dumps({
            'status': 'backward'
        })
        resp.status = falcon.HTTP_200

class CarMove:
    def on_get(self, req, resp, thrust):
        #move_backward()
        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)
        resp.body = json.dumps({
            'status': 'move',
            'thrust': thrust
            #,
            #'vector': req.params('vector')
        })
        resp.status = falcon.HTTP_200


class CarRelease:
    def on_get(self, req, resp):
        #release()
        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)
        resp.body = json.dumps({
            'status': 'stop'
        })
        resp.status = falcon.HTTP_200


class CarLightsOn:
    def on_get(self, req, resp):
        #lights_on()

        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)
        resp.body = json.dumps({
            'status': 'lights_on'
        })
        resp.status = falcon.HTTP_200


class CarLightsOff:
    def on_get(self, req, resp):
        #lights_off()

        origin = req.get_header('Origin')
        resp.set_header('Access-Control-Allow-Origin', origin)

        resp.body = json.dumps({
            'status': 'lights_off'
        })
        resp.status = falcon.HTTP_200


app = falcon.API()

app.add_route('/car/fw', CarMoveForward())
app.add_route('/car/f9/{thrust}', CarMove())
app.add_route('/car/tl', CarTurnLeft())
app.add_route('/car/tr', CarTurnRight())
app.add_route('/car/bw', CarMoveBackward())
app.add_route('/car/st', CarRelease())
app.add_route('/car/lightson', CarLightsOn())
app.add_route('/car/lightsoappff', CarLightsOff())