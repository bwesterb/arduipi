""" Web interface written using flask. """

from flask import Flask, render_template, request, jsonify
from flask_wtf.csrf import CsrfProtect

from werkzeug.wsgi import DispatcherMiddleware

import subprocess
import serial
import time

#
# Web-app written using Flask
#

app = Flask(__name__)
CsrfProtect(app)
app.config.from_pyfile('config.cfg')

wsgi_app = DispatcherMiddleware(None, {
            app.config.get('APPLICATION_ROOT', '/'): app})

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/reset', methods=['POST'])
def reset():
    """ Resets Arduino by pulling the `DTR line' low on
        the serial connection. """
    # TODO timeout if we can't open it and then reset via rPi GPIO?
    with _connect_to_arduino() as ser:
        ser.setDTR(False)
        ser.setDTR(True)
    return jsonify(ok=True)

@app.route('/api/kaku', methods=['POST'])
def kaku():
    state = request.form.get('state', 'true') == 'true'
    channel = int(request.form.get('channel', 0))
    group = request.form.get('group', 'false') == 'true'
    hwid = int(request.form.get('hwid', app.config['KAKU_HWID']))
    control_kaku(hwid, state, channel, group)
    return jsonify(ok=True)

@app.route('/api/thermistor')
def thermistor():
    return jsonify(raw=read_thermistor())

#
# Code to control the Arduino via serial port
#

def _connect_to_arduino():
    return serial.Serial(app.config['ARDUINO_TTY'], 115200)

def _radio433_transmit_ppm(pauses, pulse_length):
    """ Send pulse-position modulated signal over radio
        transmitter connected to arduino. """
    with _connect_to_arduino() as ser:
        assert ser.readline().startswith('?')
        ser.write("R{0}\n".format(len(pauses)))
        for i in xrange(len(pauses)*2-1):
            ser.write("{0}\n".format(pauses[i/2] if i%2 else pulse_length))
        assert ser.readline().startswith('!')

def control_kaku(hwid, stat=False, channel=0, group=False):
    """ Control KlikAanKlikUit devices using 433MHz transmitter on
        the arduino. """
    T = 265
    bit = {True: [5*T, T], False: [T, 5*T]}
    pulses = []
    pulses.append(T*11)
    pulses.extend(sum([bit[bool((hwid>>i) & 1)] for i in xrange(25,-1,-1)],[]))
    pulses.extend(bit[bool(group)])
    pulses.extend(bit[int(stat)])
    pulses.extend(sum([bit[bool((channel>>i) & 1)] for i in xrange(3,-1,-1)],[]))
    pulses.append(T*32)
    _radio433_transmit_ppm(pulses*3, T)

def read_thermistor():
    with _connect_to_arduino() as ser:
        assert ser.readline().startswith('?')
        ser.write('T')
        return int(ser.readline().strip())

@app.before_first_request
def arduino_tty_nohup():
    # Prevent arduino from resetting on every connection to its serial port.
    subprocess.call(['stty',  '-F', app.config['ARDUINO_TTY'], '-hup'])
    # Reset once.
    with _connect_to_arduino() as ser:
        ser.setDTR(False)
        ser.setDTR(True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
