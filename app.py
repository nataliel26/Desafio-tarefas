from bottle import  Bottle, route, run, template, get, post, request, redirect, static_file
from models import db, Task, initialize_db

app = Bottle()

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

# Rota para exibir a lista de tarefas
@app.get('/')
def index():
    tasks = Task.select()
    return template('index', tasks=tasks)

# Rota para adicionar novas tarefas
@app.post('/add')
def process_form():
   task_name = request.forms.get('task_name')
   task_description = request.forms.get('task_description')

   if task_name and task_description:
       Task.create(task_name=task_name, task_description=task_description)
       return redirect ('/')


# Rota para deletar as tarefas
@app.route('/delete/<id:int>')
def delete_task(id):
    task = Task.get(Task.id == id)
    task.delete_instance()
    return redirect ('/')

if __name__ == '__main__':
    initialize_db()
    run(app, host='localhost', port=8080, debug=True)