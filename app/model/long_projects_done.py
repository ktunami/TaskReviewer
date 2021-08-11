# python3
# -*- coding: utf-8 -*-
# @Time : 2021/8/7 10:40 
# @Author : Kate
# @File : long_projects_done.py 

from app import db


class LongProjectsDone(db.Model):
    __tablename__ = 'long_projects_done'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    content = db.Column(db.String(255))
    is_content_link = db.Column(db.Boolean, default=False)
    remarks = db.Column(db.String(255))
    done_time = db.Column(db.DATE)

    def __init__(self, id, name, content, is_content_link, remarks, done_time):
        self.id = id
        self.name = name
        self.content = content
        self.is_content_link = is_content_link
        self.remarks = remarks
        self.done_time = done_time

    def __repr__(self):
        return '<LongProjectsDone %r>' % self.name