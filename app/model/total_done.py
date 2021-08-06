# python3
# _*_ coding: utf-8 _*_
# @Time  : 2021/7/27
# @Author: Kate
# @File  : total_done.py

from app import db


class TotalDone(db.Model):
    __tablename__ = 'total_done'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), unique=True)
    learned_times = db.Column(db.Integer, default=0)
    last_time = db.Column(db.DATE)

    def __init__(self, name, learned_times, last_time):
        self.name = name
        self.learned_times = learned_times
        self.last_time = last_time

    def __repr__(self):
        return '<TotalTasks %r>' % self.name
