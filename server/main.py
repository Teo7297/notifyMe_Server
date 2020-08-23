import firebase_admin
from firebase_admin import firestore
import flask, json

app = flask.Flask(__name__)

firebase_admin.initialize_app()
USERS = firestore.client().collection('users')

@app.route('/users/register', methods=['POST'])
def add_user():
    req = flask.request.json
    user = USERS.document()
    user.set(req)
    return flask.jsonify({'id': user.id}), 201

@app.route('/users/<id>', methods=['GET'])
def read_user(id):
    return flask.jsonify(_ensure_user(id).to_dict())

@app.route('/users', methods=['GET'])
def read_users():
    users = [u.to_dict() for u in USERS.get()]
    return json.dumps(users)

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    _ensure_user(id)
    req = flask.request.json
    USERS.document(id).set(req)
    return flask.jsonify({'success': True})

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    _ensure_user(id)
    USERS.document(id).delete()
    return flask.jsonify({'success': True})

def _ensure_user(id):
    try:
        return USERS.document(id).get()
    except:
        flask.abort(404)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)