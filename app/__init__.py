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

from app.model import total_tasks, daily_tasks, tips_record
from app.model import today_work, long_term_items, recent_items, long_projects_done

if app.config.get('DATABASE_INITIALIZATION'):
    db.drop_all()
    db.create_all()

from app.controller import web_views
