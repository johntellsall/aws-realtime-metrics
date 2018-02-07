from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response

CAT_DATABASE = [
'https://s7d1.scene7.com/is/image/PETCO/cat-category-090617-369w-269h-hero-cutout-d'
]
PAGE_HTML = '''
<img src="{image_url}">
'''

def hello_world(request):
	cat_url = CAT_DATABASE[0]
	return Response(PAGE_HTML.format(image_url=cat_url))

if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')
        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8000, app)
    server.serve_forever()
