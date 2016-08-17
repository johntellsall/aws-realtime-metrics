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


logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
    handlers = {
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
        },
    loggers = {
        'engineio': {'level': logging.ERROR},
        'socketio': {'level': logging.ERROR},
        },
    root = {
        'handlers': ['h'],
        'level': logging.DEBUG,
        },
)
logging.config.dictConfig(logging_config)

def create_app():
    myapp = Flask(__name__)
    myapp.config['SECRET_KEY'] = 'secret!'
    return myapp

app = create_app()
redis_store = redis.StrictRedis(host='localhost', port=6379, db=0)
socketio = SocketIO(app)

thread = None


def background_thread():
    while True:
        socketio.sleep(10)
        time_str = datetime.datetime.now().strftime('%H:%M:%S')
        stats = redis_store.hgetall('stats')
        response = {'stats': stats, 'time': time_str}
        logging.debug('response: %s', response)
        socketio.emit('my response', response, namespace='/test')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@app.route('/vote', methods=['POST'])
def vote():
    app.logger.info('vote: %s', request.values['value'])
    return OK_RESPONSE

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


# @socketio.on_error_defaulthandler
# def default_error_handler(err):
#     print 'UHOH', err
#     logging.error('socketio: %s', err)


if __name__ == '__main__':
    if 1:
        socketio.run(app, debug=True, use_reloader=True)
    else:
        import eventlet
        sio = socketio.server.Server(async_mode='eventlet')
        s_app = socketio.Middleware(sio, app)
        eventlet.wsgi.server(eventlet.listen(('', 5000)), s_app)
