# python3
# _*_ coding: utf-8 _*_
# @Time  : 2021/7/27
# @Author: Kate
# @File  : __init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_pyfile('./setting.py')

db = SQLAlchemy(app)

from app.model import total_tasks, daily_tasks, total_done, today_work

if app.config.get('DATABASE_INITION'):
    db.drop_all()
    db.create_all()

from app.controller import web_views
