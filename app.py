from bottle import  Bottle, route, run, template, get, post, request, redirect, static_file, response
from models import db, User, Task, initialize_db
from functools import wraps
import requests_oauthlib
import bcrypt
import jwt

app = Bottle()

secret = "nat123"

<<<<<<< HEAD
def session():
    try:
        user = request.get_cookie('AUTH', None)
        return user
    except:
        return None
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
=======
def signed_in():
    @wraps()
    def user():
        token = request.get_cookie('AUTH', None)

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             


>>>>>>> ad03d05db41728ebd2d989598d97b6af7257c48c
def protected(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.get_cookie('AUTH', None)
        
        if not token:
            response.status = 401
            return redirect('/signin')
        
        try:
            decoded = jwt.decode(token, secret, algorithms=["HS256"])
            request.user = decoded['username']
        except jwt.InvalidTokenError:
            response.status = 401
            return redirect('/signin')
        
        return f(*args, **kwargs)
    return decorated

def create_token(username):
    payload = {
        'username': username
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return token

def tasks_to_dict(task):
    return {
        'id': task.id,
        'name': task.task_name,
        'description': task.task_description
    }

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

# Rota para exibir o formulário de cadastro
@app.get('/signup')
def signup_page():
    return template('account', signup=True)

# Rota para criação de conta
@app.post('/signup')
def signup():
    username = request.forms.get('username')
    password = request.forms.get('password')
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    User.create(username=username, password=hashed_password.decode('utf-8'))
    return redirect('/')

@app.get('/signin')
def signin_page():
    return template('account', signup=None)

@app.post('/signin')
def signin():
    username = request.forms.get('username')
    password = request.forms.get('password')

    try:
        user = User.get(User.username == username)
    except User.DoesNotExist:
        response.status = 400
        return "Usuário inválido"
    if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        response.status = 400
        return "Senha inválida"
    
    token = create_token(user.username)
    response.set_cookie('AUTH', token)
    return redirect ('/')

@app.get('/logout')
def logout():
    response.delete_cookie('AUTH')
    return redirect('/')


# Rota para exibir a lista de tarefas
@app.get('/')
def index():
    session = request.get_cookie('AUTH', None)
    tasks = Task.select()
    if not session:
        return template('index', tasks=tasks, edit_task=None, session=None)
    return template('index', tasks=tasks, edit_task=None, session=True)

# Rota para exibir as tarefas em formato application/json
@app.get('/api/v1/tasks')
def get_tasks():
    tasks = Task.select()
    tasks_list = [tasks_to_dict(task) for task in tasks]
    response.content_type = 'application/json'
    return {'tarefas' : tasks_list}

# Rota para adicionar novas tarefas
@app.post('/add')
@protected
def add_task():
   user = request.get_cookie('AUTH', None)
   task_name = request.forms.get('task_name')
   task_description = request.forms.get('task_description')
<<<<<<< HEAD
   user = request.get_cookie('AUTH', None)
=======
>>>>>>> ad03d05db41728ebd2d989598d97b6af7257c48c
   Task.create(task_name=task_name, task_description=task_description, user=user)
   return redirect('/')

# Rota para adicionar novas tarefas com json
@app.post('/api/v1/tasks')
@protected
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
@protected
def edit_task(id):
    task = Task.get(Task.id == id)
    tasks = Task.select()
    return template('index', tasks=tasks,edit_task=task)

# Rota para editar tarefas
@app.post('/edit/<id:int>')
@protected
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
@protected
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
@protected
def delete_task(id):
    task = Task.get(Task.id == id)
    task.delete_instance()
    return redirect ('/')

# Rota para deletar as tarefas pelo id
@app.delete('/api/v1/tasks/<id:int>')
@protected
def delete_task_json(id):
    task = Task.get(Task.id == id)
    task.delete_instance()
    response.status = 200
    return response


if __name__ == '__main__':
    initialize_db()
    run(app, host='localhost', port=8080, reloader=True, debug=True)