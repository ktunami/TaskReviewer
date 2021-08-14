# python3
# -*- coding: utf-8 -*-
# @Time : 2021/8/14 12:52 
# @Author : Kate
# @File : links_record.py
from sqlalchemy import ForeignKey

from app import db


class LinksRecord(db.Model):
    __tablename__ = 'links_record'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tip_id = db.Column(db.Integer, ForeignKey('tips_record.id', ondelete='CASCADE'))
    content = db.Column(db.String(200))
    remarks = db.Column(db.Text())

    def __init__(self, tip_id, content, remarks):
        self.tip_id = tip_id
        self.content = content
        self.remarks = remarks

    def __repr__(self):
        return '<LinksRecord %r>' % self.remarks

