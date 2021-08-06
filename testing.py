# python3
# _*_ coding: utf-8 _*_
# @Time  : 2021/7/27
# @Author: Kate
# @File  : testing.py

from app import db
from app.model.long_term_items import LongTermItems
from app.model.total_tasks import TotalTasks
from app.model.daily_tasks import DailyTasks
import datetime


def get_date(str_name):
    return datetime.datetime.strptime(str_name, "%Y-%m-%d")


def add_total_tasks():
    in_date1 = '2021-07-30'
    item1 = TotalTasks(name="语文2", next_begin_time=get_date(in_date1),
                       progress=0)
    item2 = TotalTasks(name="数学2", next_begin_time=get_date(in_date1),
                       progress=0)
    item3 = TotalTasks(name="英语2", next_begin_time=get_date(in_date1),
                       progress=10)
    db.session.add_all([item1, item2, item3])
    db.session.commit()


def add_long_tasks():
    in_date1 = '2021-08-5'
    item1 = LongTermItems(
        name="语文2",
        content="纸质书(已打印)",
        remarks="无",
        expected_begin_time="",
        expected_end_time="",
        already_begin=True,
        is_content_link=False
    )
    item2 = LongTermItems(
        name="数学2",
        content="纸质书(已打印)",
        remarks="无",
        expected_begin_time="",
        expected_end_time="",
        already_begin=False,
        is_content_link=False
    )
    db.session.add_all([item1, item2])
    db.session.commit()


def add_new_learned():
    in_date = '2021-07-27'
    dt = datetime.datetime.strptime(in_date, "%Y-%m-%d")
    # out_date = (dt + datetime.timedelta(days=2)).strftime("%Y-%m-%d")

    item1 = DailyTasks(total_task_id=1, name="语文第8章",
                       next_begin_time=dt, progress=10)
    item2 = DailyTasks(total_task_id=2, name="数学第8章",
                       next_begin_time=dt, progress=10)
    item3 = DailyTasks(total_task_id=3, name="英语第8章",
                       next_begin_time=dt, progress=10)
    db.session.add_all([item1, item2, item3])
    db.session.commit()


def delete_items(table_class):
    t = table_class.query.all()
    for i in t:
        db.session.delete(i)
        db.session.commit()


if __name__ == '__main__':
    add_long_tasks()
