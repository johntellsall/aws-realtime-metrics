# USAGE
#   FLASK_APP=rhappy.py flask run


import redis
from flask import Flask

app = Flask(__name__)
redis_store = redis.StrictRedis(host='localhost', port=6379, db=0)


@app.route('/')
def index():
    return redis_store.get('beer')

