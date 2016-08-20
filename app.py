#!/usr/bin/env python

# USAGE
# fuser -k 5000/tcp ; FLASK_APP=app.py flask run

import json

import redis
from flask import Flask, render_template, request
from flask_socketio import SocketIO


def json_response(data):
    return json.dumps(data), 200, {'ContentType':'application/json'}

def create_app():
    myapp = Flask(__name__)
    myapp.config['SECRET_KEY'] = 'secret!'
    return myapp

def init_db(redis_db):
    redis_db.set('votes', 0)

app = create_app()
redis_store = redis.StrictRedis(host='localhost', port=6379, db=0)
socketio = SocketIO(app, async_mode='gevent')

thread = None


def get_votes_dict():
    return redis_store.hgetall('vote')


def background_thread():
    while True:
        socketio.sleep(10)
        vdict = get_votes_dict()
        app.logger.debug('votes dict: %s', vdict)
        socketio.emit('my response', vdict, namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        vote_value = request.values['value']
        if vote_value not in ('up', 'down'):
            return None # TODO return 400
        redis_store.hincrby('vote', 'count', 1)
        if vote_value == 'up':
            redis_store.hincrby('vote', 'up_count', 1)
    vdict = get_votes_dict()
    socketio.emit('my response', vdict, namespace='/test')
    return json_response(vdict)


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    app.logger.info('sid=%s: Client disconnected', request.sid)


@socketio.on_error_default
def default_error_handler(err):
    app.logger.error('UHOH: %s', err)


if __name__ == '__main__':
    init_db(redis_store)
    socketio.run(app, debug=True, use_reloader=True)
