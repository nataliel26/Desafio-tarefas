from peewee import *

db = SqliteDatabase ('tasks.db')

class Task(Model):
    task_name = CharField ()
    task_description = TextField ()
    
    class Meta:
        database = db




    