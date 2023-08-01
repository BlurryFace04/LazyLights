from flask import Flask, render_template, request
import RPi.GPIO as GPIO
import jyserver.Flask as jsf
import netifaces as ni

app = Flask(__name__)

bl = 2
f = 3
s = 4
tl = 17
d = 14

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(bl, GPIO.OUT)
GPIO.setup(f, GPIO.OUT)
GPIO.setup(s, GPIO.OUT)
GPIO.setup(tl, GPIO.OUT)
GPIO.setup(d, GPIO.OUT)


@jsf.use(app)
class App:
    def back_light(self):
        if GPIO.input(bl) == 0:
            GPIO.output(bl, 1)
        else:
            GPIO.output(bl, 0)

    def fan(self):
        if GPIO.input(f) == 0:
            GPIO.output(f, 1)
        else:
            GPIO.output(f, 0)

    def socket(self):
        if GPIO.input(s) == 0:
            GPIO.output(s, 1)
        else:
            GPIO.output(s, 0)

    def top_light(self):
        if GPIO.input(tl) == 0:
            GPIO.output(tl, 1)
        else:
            GPIO.output(tl, 0)

    def door(self):
        if GPIO.input(d) == 0:
            GPIO.output(d, 1)
        else:
            GPIO.output(d, 0)

    def back_light_esp(self):
        if GPIO.input(bl) == 0:
            GPIO.output(bl, 1)
        else:
            GPIO.output(bl, 0)

    def fan_esp(self):
        if GPIO.input(f) == 0:
            GPIO.output(f, 1)
        else:
            GPIO.output(f, 0)

    def socket_esp(self):
        if GPIO.input(s) == 0:
            GPIO.output(s, 1)
        else:
            GPIO.output(s, 0)

    def top_light_esp(self):
        if GPIO.input(tl) == 0:
            GPIO.output(tl, 1)
        else:
            GPIO.output(tl, 0)

    def door_esp(self):
        if GPIO.input(d) == 0:
            GPIO.output(d, 1)
        else:
            GPIO.output(d, 0)


@app.route("/")
def index():
    return App.render(render_template("index.html"))


@app.route("/jsonex", methods=['POST'])
def jsonex():
    request_data = request.get_json()

    appliance = request_data['appliance']
    print(appliance)

    if appliance == "bl":
        App.back_light_esp()

    if appliance == "tl":
        App.top_light_esp()

    if appliance == "f":
        App.fan_esp()

    if appliance == "s":
        App.socket_esp()

    if appliance == "d":
        App.door_esp()

    return ("Appliance is {}".format(appliance))


if __name__ == "__main__":
    print("start")
    app.run(host="0.0.0.0", port=5069)
