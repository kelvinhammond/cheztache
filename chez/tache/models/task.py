
from sqlalchemy import sql
from .base import db, Base
from .project import Project


def default_task_number(context):
    return context.connection.execute(
        sql.select([sql.func.ifnull(sql.func.max(Task.number), 0) + 1])
    ).scalar()


class Task(Base):
    PRIORITY_VALUES = (
        (u'l', u'Low'),
        (u'm', u'Medium'),
        (u'h', u'High'),
    )

    project_id = db.Column(db.UUID(binary=False), db.ForeignKey(Project.id))
    project = db.relationship(Project,
                              backref=db.backref("tasks", lazy='dynamic'))

    description = db.Column(db.UnicodeText, nullable=False)
    priority = db.Column(db.Choice(PRIORITY_VALUES))
    due = db.Column(db.Arrow)
    waituntil = db.Column(db.Arrow)
    completed = db.Column(db.Arrow)

    number = db.Column(db.Integer, unique=True, default=default_task_number)
