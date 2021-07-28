from app import db


class DailyTasks(db.Model):
    __tablename__ = 'daily_tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_task_id = db.Column(db.Integer, db.ForeignKey('total_tasks.id'))
    name = db.Column(db.String(64), unique=True)
    learned_times = db.Column(db.Integer, default=0)
    last_time = db.Column(db.DATE)
    next_begin_time = db.Column(db.DATE, index=True)
    progress = db.Column(db.Integer, default=0)

    def __init__(self, total_task_id, name, next_begin_time, progress):
        self.total_task_id = total_task_id
        self.name = name
        self.next_begin_time = next_begin_time
        self.progress = progress

    def __repr__(self):
        return '<DailyTasks %r>' % self.name
