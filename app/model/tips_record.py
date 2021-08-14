# python3
# _*_ coding: utf-8 _*_
# @Time  : 2021/7/27
# @Author: Kate
# @File  : tips_record.py

from app import db


class TipsRecord(db.Model):
    __tablename__ = 'tips_record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    instruction = db.Column(db.Text())

    def __init__(self, name, instruction):
        self.name = name
        self.instruction = instruction

    def __repr__(self):
        return '<TipsRecord %r>' % self.name


