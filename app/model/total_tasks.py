# python3
# _*_ coding: utf-8 _*_
# @Time  : 2021/7/27
# @Author: Kate
# @File  : total_tasks.py

from app import db


class TotalTasks(db.Model):
    __tablename__ = 'total_tasks'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(200), unique=True)
    learned_times = db.Column(db.Integer, default=0)
    next_begin_time = db.Column(db.DATE)
    progress = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DATE)

    def __init__(self, project_id, name, next_begin_time, progress, create_time):
        self.id = project_id
        self.name = name
        self.next_begin_time = next_begin_time
        self.progress = progress
        self.create_time = create_time

    def __repr__(self):
        return '<TotalTasks %r>' % self.name
