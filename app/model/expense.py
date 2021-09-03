# python3
# -*- coding: utf-8 -*-
# @Time : 2021/9/1 19:54 
# @Author : Kate
# @File : expense.py.py 
# @

from app import db
from app.model.common_checks import *


class Expense(db.Model):
    __tablename__ = 'expense'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category = db.Column(db.String(64))
    sub_category = db.Column(db.String(64))
    content = db.Column(db.String(255))
    money = db.Column(db.DECIMAL())
    create_date = db.Column(db.DATE)

    def __init__(self, category, sub_category, content, money, create_date):
        self.category = category
        self.sub_category = sub_category
        self.content = content
        self.money = money
        self.create_date = create_date

    def __repr__(self):
        return '<Expense %r>' % self.category

    def keys(self):
        return 'category', 'sub_category', 'content', 'money', 'create_date'

    def __getitem__(self, item):
        return getattr(self, item)

