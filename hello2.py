import logging
import sys
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


PORT = 8080
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)


def hello_world(request):
    return Response('Hello %(name)s!' % request.matchdict)


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/hello/{name}')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    logging.info('Running on port %d', PORT)
    server = make_server('0.0.0.0', PORT, app)
    server.serve_forever()
