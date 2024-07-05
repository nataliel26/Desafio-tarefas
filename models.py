from peewee import *
from playhouse.migrate import *

db = SqliteDatabase ('tasks.db')
migrator = SqliteMigrator(db)


class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    user_id = AutoField()
    username = CharField(unique=True)
    password = CharField()

class Task(BaseModel):
    task_name = CharField ()
    task_description = TextField ()
    user = ForeignKeyField(User, field='username', backref='tasks', default=User)


def initialize_db():
    db.connect()
    db.create_tables([User, Task], safe = True)
    db.close()

