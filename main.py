from bottle import route, run, template
from tasks import db, Task

@route('/')
def hello():
    return "Hello world"

run(host='localhost', port=8080, debug=True)