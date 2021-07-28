
from app import db
import datetime


class TodayWork(db.Model):
    __tablename__ = 'today_work'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    total_task_id = db.Column(db.Integer)
    total_task_name = db.Column(db.String(64))
    name = db.Column(db.String(64), unique=True)
    today_date = db.Column(db.DATE, default=datetime.datetime.today().date())
    progress = db.Column(db.Integer, default=0)

    def __init__(self, total_task_id, total_task_name, name, progress):
        self.total_task_id = total_task_id
        self.total_task_name = total_task_name
        self.name = name
        self.progress = progress


    def __repr__(self):
        return '<TodayWork %r>' % self.name
