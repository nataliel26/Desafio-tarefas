from bottle import  Bottle, route, run, template, get, post, request, static_file
from tasks import Task, initialize_db

app = Bottle()
initialize_db()


@app.route('/')
def index():
    return template('views/index.html')

@post('/add', method = 'POST')
def process_form():
   task_name = request.forms.get('task')
   task_description = request.forms.get('description')
   if task_name:
       Task.create(task_name = task_name)

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)