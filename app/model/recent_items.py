# python3
# -*- coding: utf-8 -*-
# @Time : 2021/8/5 12:00 
# @Author : Kate
# @File : recent_items.py

from app import db
from app.model.common_checks import *


class RecentItems(db.Model):
    __tablename__ = 'recent_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    content = db.Column(db.String(255))
    is_content_link = db.Column(db.Boolean, default=False)
    remarks = db.Column(db.String(255))
    create_date = db.Column(db.DATE)
    start_time = db.Column(db.TIME, index=True)
    end_time = db.Column(db.TIME)
    expected_days = db.Column(db.Integer, default=1, index=True)
    already_complete = db.Column(db.Boolean, default=False)
    complete_date = db.Column(db.DATE)

    def __init__(self, name, content, is_content_link, remarks, expected_days, create_date, start_time, end_time):
        self.name = name
        self.content = content
        self.is_content_link = is_content_link
        self.remarks = remarks
        self.expected_days = get_num(expected_days, 1)
        self.create_date = create_date
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return '<RecentItems %r>' % self.name
