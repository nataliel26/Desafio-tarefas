from bottle import  Bottle, route, run, template, get, post, request, redirect, static_file
from models import db, Task

app = Bottle()

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

@app.get('/')
def index():
    tasks = Task.select()
    return template('index', tasks=tasks)

@app.post('/add')
def process_form():
   task_name = request.forms.get('task_name')
   task_description = request.forms.get('task_description')

   if task_name and task_description:
       Task.create(task_name=task_name, task_description=task_description)
       return redirect('/')

db.connect()
db.create_tables([Task])

for route in app.routes:
    print(route.rule)

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)