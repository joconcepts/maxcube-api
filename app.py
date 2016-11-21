#!/usr/bin/python3.5
from flask import Flask, jsonify, abort, request
from maxcube.cube import MaxCube
from maxcube.connection import MaxCubeConnection

cube = MaxCube(MaxCubeConnection('192.168.1.200', 62910))

app = Flask(__name__)

@app.route('/cube', methods=['GET','POST'])
def cube_update():
    if request.method == 'POST':
        cube.update()
    return jsonify(cube.todict())

@app.route('/cube/ntp', methods=['GET', 'POST'])
def ntp():
    if request.method == 'POST':
        a = cube.ntp_servers(request.json["ntp_servers"])
    else:
        a = cube.ntp_servers()
    return jsonify({"ntp_servers": a.ntp_servers})

@app.route('/devices', methods=['GET', 'POST'])
def get_devices():
    if request.method == 'POST':
        cube.refresh_devices()

    out = []
    for device in cube.devices:
        out.append(device.todict())
    return jsonify(out)

@app.route('/devices/<string:rf_address>', methods=['GET'])
def get_device(rf_address):
    ref = request.args.get('refresh')
    if ref and ref == 'true':
        cube.refresh_devices()
    d = cube.device_by_rf(rf_address)
    if not d:
        abort(404)
    return jsonify(d.todict())

@app.route('/devices/<string:rf_address>', methods=['POST'])
def set_defice(rf_address):
    print(request.json)
    d = cube.device_by_rf(rf_address)
    if not d:
        abort(404)
    r = d.set_temperature(request.json["temperature"])
    r.device = r.device.todict()
    return jsonify(r.__dict__)

@app.route('/rooms')
def get_rooms():
    out = []
    for room in cube.rooms:
        out.append(room.__dict__)
    return jsonify(out)

@app.route('/rooms/<int:room_id>')
def get_room(room_id):
    r = cube.room_by_id(room_id)
    if not r:
        abort(404)
    return jsonify(r.__dict__)


if __name__ == '__main__':
    app.run(debug=True)
