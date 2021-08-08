# python3
# -*- coding: utf-8 -*-
# @Time : 2021/8/5 11:24 
# @Author : Kate
# @File : long_term_items.py 


from app import db
from app.model.common_checks import *


class LongTermItems(db.Model):
    __tablename__ = 'long_term_items'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    content = db.Column(db.String(255))
    is_content_link = db.Column(db.Boolean, default=False)
    remarks = db.Column(db.String(255))
    expected_begin_time = db.Column(db.DATE)
    expected_end_time = db.Column(db.DATE)
    already_begin = db.Column(db.Boolean, default=False, index=True)
    already_complete = db.Column(db.Boolean, default=False)
    done_times = db.Column(db.Integer, default=0, index=True)
    add_to_study = db.Column(db.Boolean, default=False)

    def __init__(self, name, content, is_content_link, remarks, expected_begin_time, expected_end_time):
        self.name = name
        self.content = content
        self.is_content_link = is_content_link
        self.remarks = remarks
        self.expected_begin_time = get_date(expected_begin_time)
        self.expected_end_time = get_date(expected_end_time)

    def __repr__(self):
        return '<LongTermItems %r>' % self.name


