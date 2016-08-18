#!/usr/bin/env python

# USAGE
# fuser -k 5000/tcp ; FLASK_APP=app.py flask run

import datetime
import json
import logging
import logging.config

import redis
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect


OK_RESPONSE = (json.dumps({'success':True}), 200, 
    {'ContentType':'application/json'} )
def json_response(data):
    return json.dumps(data), 200, {'ContentType':'application/json'}

# logging_config = dict(
#     version = 1,
#     formatters = {
#         'f': {'format':
#               '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
#         },
#     handlers = {
#         'h': {'class': 'logging.StreamHandler',
#               'formatter': 'f',
#               'level': logging.DEBUG}
#         },
#     loggers = {
#         'engineio': {'level': logging.ERROR},
#         'socketio': {'level': logging.ERROR},
#         },
#     root = {
#         'handlers': ['h'],
#         'level': logging.DEBUG,
#         },
# )
# logging.config.dictConfig(logging_config)

def create_app():
    myapp = Flask(__name__)
    myapp.config['SECRET_KEY'] = 'secret!'
    return myapp

def init_db(redis_db):
    redis_db.set('votes', 0)

app = create_app()
redis_store = redis.StrictRedis(host='localhost', port=6379, db=0)
socketio = SocketIO(app)

thread = None


def get_votes_dict():
    return redis_store.hgetall('vote')


def background_thread():
    while True:
        socketio.sleep(10)
        vdict = get_votes_dict()
        logging.debug('votes dict: %s', vdict)
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
    return json_response(vdict)


@socketio.on('my event', namespace='/test')
def test_message(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    emit('my response',
         {'data': message['data'], 'count': session['receive_count']})


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
    emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    init_db(redis_store)
    socketio.run(app, debug=True, use_reloader=True)
