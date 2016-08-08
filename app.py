#!/usr/bin/env python

import datetime
import logging
import sys

import redis
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect

logging.basicConfig(stream=sys.stderr) # , level=logging.DEBUG)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
redis_store = redis.StrictRedis(host='localhost', port=6379, db=0)
thread = None


def background_thread():
    """Example of how to send server generated events to clients."""
    while True:
        socketio.sleep(10)
        time_str = datetime.datetime.now().strftime('%H:%M:%S')
        stats = redis_store.hgetall('stats')
        response = {'stats': stats, 'time': time_str}
        socketio.emit('my response', response, namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


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
    socketio.run(app, debug=True)
