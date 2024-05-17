from peewee import (Model, 
                    SqliteDatabase, 
                    TextField, 
                    IntegerField, 
                    AutoField, 
                    DateTimeField, 
                    ForeignKeyField, 
                    CharField, 
                    TimeField, 
                    DateField)


class ProjectStatus:
    NOT_STARTED = 'N'
    IN_PROCESS = 'P'
    COMPLETED = 'C'
    DELAYED = 'D'


db = SqliteDatabase('resourses\\worknotes.db')
db.connect()

class BaseModel(Model):
    class Meta:
        database = db
        
        
    
class WorkSpace(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField(null=False, default='Доска')
    
class Project(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField(null=False)
    description = TextField(null=True)
    comment = TextField(null=True)
    start_date = DateTimeField(['%Y-%m-%d'], null=False)
    deadline = DateTimeField(['%Y-%m-%d'], null=False)
    spend_time = TextField(null=False,) # h.m/day
    status = CharField(160, null=False)
    board_id = ForeignKeyField(WorkSpace, on_delete='CASCADE')
    
class Task(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField(null=False)
    description = TextField(null=True)
    total_time = IntegerField(null=False)
    deadline = DateTimeField(['%Y-%m-%d'], null=False)
    project_id = ForeignKeyField(Project, on_delete='CASCADE')
    
    
class Calendar(BaseModel):
    id = AutoField(primary_key=True)
    type = TextField(null=False)
    
class Event(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField(null=False)
    type = TextField(null=False)
    date = DateField(['%Y-%m-%d'], null=False)
    time = TimeField(['%H:%M'], null=True)
    description = TextField(null=True)
    calendar_id = ForeignKeyField(Calendar, on_delete='CASCADE', on_update='CASCADE')
    
    
db.create_tables([Task, Project, WorkSpace, Event, Calendar])
