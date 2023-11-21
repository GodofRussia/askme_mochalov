# from cgi import parse_qs, escape
from urllib.parse import parse_qs

HELLO_WORLD = b"Hello world!\n"


def app(environ, start_response):
    """Simplest possible application object"""
    status = '200 OK'
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0
    print(environ['REQUEST_METHOD'])
    if environ['REQUEST_METHOD'] == "GET":
        d = parse_qs(environ['QUERY_STRING'])
        print(d)
    elif environ['REQUEST_METHOD'] == "POST":
        request_body = environ['wsgi.input'].read(request_body_size)
        d = parse_qs(request_body)
        print(d)
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [HELLO_WORLD]


# httpd = make_server('localhost', 8081, application)
# httpd.serve_forever()	
