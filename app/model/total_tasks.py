from app import db

class TotalTasks(db.Model):

    __tablename__ = 'total_tasks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True)
    learned_times = db.Column(db.Integer, default=0)
    next_begin_time = db.Column(db.DATE)
    progress = db.Column(db.Integer, default=0)

    def __init__(self, name, next_begin_time, progress):
        self.name = name
        self.next_begin_time = next_begin_time
        self.progress = progress

    def __repr__(self):
        return '<TotalTasks %r>' % self.name

