from peewee import *

db = SqliteDatabase ('tasks.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()

class Task(BaseModel):
    task_name = CharField ()
    task_description = TextField ()

def initialize_db():
    db.connect()
    db.create_tables([Task], safe=True)
    db.close()



    