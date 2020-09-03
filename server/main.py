import firebase_admin
from firebase_admin import firestore
import flask, json
#import os
#os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/teo/Desktop/notifyMe_Server/NotifyMe-1acab18a931f.json"
app = flask.Flask(__name__)

firebase_admin.initialize_app()
DEVICES = firestore.client().collection('devices')

@app.route('/new_device', methods=['POST'])
def add_user():
    req = flask.request.json
    device = DEVICES.document()
    device.set(req)
    return flask.jsonify({'token': device.token}), 201

@app.route('/devices/<token>', methods=['GET'])
def read_devie(token):
    return flask.jsonify(_ensure_device(token).to_dict())

@app.route('/devices', methods=['GET'])
def read_devices():
    devices = [d.to_dict() for d in DEVICES.get()]
    return json.dumps(devices)

@app.route('/devices/<token>', methods=['PUT'])
def update_device(token):
    _ensure_device(token)
    req = flask.request.json
    DEVICES.document(token).set(req)
    return flask.jsonify({'success': True})

@app.route('/devices/<token>', methods=['DELETE'])
def delete_device(token):
    _ensure_device(token)
    DEVICES.document(token).delete()
    return flask.jsonify({'success': True})

def _ensure_device(token):
    try:
        return DEVICES.document(token).get()
    except:
        flask.abort(404)

if __name__ == '__main__':
    
    app.run(host='127.0.0.1', port=8080, debug=True)