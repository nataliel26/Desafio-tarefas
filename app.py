from bottle import  Bottle, route, run, template, get, post, request, redirect, static_file, response
from models import db, Task, initialize_db

app = Bottle()

def tasks_to_dict(task):
    return {
        'id': task.id,
        'name': task.task_name,
        'description': task.task_description
    }

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

# Rota para exibir a lista de tarefas
@app.get('/')
def index():
    tasks = Task.select()
    return template('index', tasks=tasks, edit_task=None)

# Rota para exibir as tarefas em formato application/json
@app.get('/api/v1/tasks')
def get_tasks():
    tasks = Task.select()
    tasks_list = [tasks_to_dict(task) for task in tasks]
    response.content_type = 'application/json'
    return {'tarefas' : tasks_list}

# Rota para adicionar novas tarefas
@app.post('/add')
def add_task():
   task_name = request.forms.get('task_name')
   task_description = request.forms.get('task_description')
   Task.create(task_name=task_name, task_description=task_description)
   return redirect('/')

# Rota para adicionar novas tarefas com json
@app.post('/api/v1/tasks')
def add_task_json():
   task_data = request.json
   new_task = Task.create(
       task_name=task_data['name'],
       task_description=task_data.get('description', '')
   )
   response.content_type = 'application/json'
   response.status = 201
   return tasks_to_dict(new_task)

# Rota para seleção da tarefa a ser editada
@app.route('/edit/<id:int>')
def edit_task(id):
    task = Task.get(Task.id == id)
    tasks = Task.select()
    return template('index', tasks=tasks,edit_task=task)

# Rota para editar tarefas
@app.post('/edit/<id:int>')
def update_task(id):
    task_name = request.forms.get('task_name')
    task_description = request.forms.get('task_description')
    task = Task.get(Task.id == id)
    task.task_name = task_name
    task.task_description = task_description
    task.save()
    return redirect('/')

# Rota para edição de tarefas usando json
@app.put('/api/v1/tasks/<id:int>')
def edit_task_json(id):
    task = Task.get(Task.id == id)
    task_data = request.json
    task.task_name=task_data['name']
    task.task_description=task_data.get('description', '')
    task.save()
    response.content_type = 'application/json'
    return tasks_to_dict(task)

# Rota para deletar as tarefas
@app.route('/delete/<id:int>')
def delete_task(id):
    task = Task.get(Task.id == id)
    task.delete_instance()
    return redirect ('/')

# Rota para deletar as tarefas pelo id
@app.delete('/api/v1/tasks/<id:int>')
def delete_task_json(id):
    task = Task.get(Task.id == id)
    task.delete_instance()
    response.status = 200
    return response


if __name__ == '__main__':
    initialize_db()
    run(app, host='localhost', port=8080, reloader=True, debug=True)