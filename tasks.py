from peewee import *

db = SqliteDatabase ('tasks.db')

class Task(Model):
    task_name = CharField ()
    task_description = TextField ()
    
    class Meta:
        database = db

def initialize_db():
    db.connect()
    db.create_tables([Task], safe=True)
    db.close()



    