# python3
# _*_ coding: utf-8 _*_
# @Time  : 2021/7/27
# @Author: Kate
# @File  : setting.py


# ------------ Basic Database Setting  ------------
DIALECT = 'mysql'
DRIVER = 'mysqlconnector'
USERNAME = 'root'
PASSWORD ='hello123'
HOST = 'localhost'
PORT ='3306'
DATABASE = 'task_reviewer'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

# ------------  Other Settings  ------------
DEBUG = True
DATABASE_INITION = False                        # Drop and recreate all tables in database
REVIEW_RULES = {1:1,                            # Review rules of daily tasks
                2:1,                               # key -> the ith review
                3:5,                               # value -> review interval
                4:8}

TOTAL_REVIEW_RULES = {1:45,                     # Review rules of total tasks
                      2:60}                        # key -> the ith review
                                                   # value -> review interval

WEEKDAYS_DISPLAY = {0:"周一", 1:"周二", 2:"周三", 3:"周四", 4:"周五", 5:"周六", 6:"周日"}