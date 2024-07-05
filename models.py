from peewee import *
from playhouse.migrate import *

db = SqliteDatabase ('tasks.db')
migrator = SqliteMigrator(db)


class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField(unique=True)
    password = CharField()

class Task(BaseModel):
    task_name = CharField ()
    task_description = TextField ()
    user = ForeignKeyField(User, field='username', backref='tasks', default='Nenhum')

def initialize_db():
    if db.is_closed():
        db.connect()
    db.create_tables([User, Task], safe = True)
    db.close()

existing_columns = [column.name for column in db.get_columns('task')]
if 'user' not in existing_columns:
    migrate(
        migrator.add_column('task', 'user', Task.user)
    )

def migrate_db():
    existing_columns = [column.name for column in db.get_columns('task')]
    if 'user' not in existing_columns:
        migrate(
            migrator.add_column('task', 'user', Task.user)
        )
