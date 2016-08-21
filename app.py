#!/usr/bin/env python

# USAGE
# fuser -k 5000/tcp ; python app.py

import json

import redis
from flask import Flask, g, render_template, request
from flask_socketio import SocketIO


def create_app():
    myapp = Flask(__name__)
    myapp.config['SECRET_KEY'] = 'secret!'
    return myapp


class VoteStore(object):
    def __init__(self):
        self.db = redis.StrictRedis()

    def reset(self):
        self.db.set('votes', 0)

    def get_all(self):
        return self.db.hgetall('vote')

    def vote(self, up):
        self.db.hincrby('vote', 'count', 1)
        if up:
            self.db.hincrby('vote', 'up_count', 1)

app = create_app()
socketio = SocketIO(app, async_mode='gevent')
vote_db = VoteStore()
vote_db.reset()

thread = None



def json_response(data):
    return json.dumps(data), 200, {'ContentType':'application/json'}


def background_thread():
    '''
    send all votes to all clients
    '''
    while True:
        socketio.sleep(10)
        vdict = vote_db.get_all()
        app.logger.debug('votes dict: %s', vdict)
        socketio.emit('votes', vdict, namespace='/vote')


@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if request.method == 'POST':
        vote_value = request.values['value']
        if vote_value not in ('up', 'down'):
            return None # TODO return 400
        vote_db.vote(up=(vote_value == 'up'))
    vdict = vote_db.get_all()
    socketio.emit('votes', vdict, namespace='/')
    return json_response(vdict)


@socketio.on('connect', namespace='')
def test_connect():
    global thread
    app.logger.info('sid=%s: Client connected', request.sid)
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)


@socketio.on('disconnect', namespace='')
def test_disconnect():
    app.logger.info('sid=%s: Client disconnected', request.sid)


@socketio.on_error_default
def default_error_handler(err):
    app.logger.error('UHOH: %s', err)


# # @app.cli.command('initdb')
# def initdb_command():
#     vote_d = VoteStore()
#     vote_d.reset()


if __name__ == '__main__':
    socketio.run(app, debug=True, use_reloader=True)
