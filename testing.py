from app import db
from app.model.total_tasks import TotalTasks
from app.model.daily_tasks import DailyTasks
import datetime


def add_total_tasks():
    item1 = TotalTasks(name="语文", next_begin_time=datetime.datetime.today().date(),
                       progress=10)
    item2 = TotalTasks(name="数学", next_begin_time=datetime.datetime.today().date(),
                       progress=10)
    item3 = TotalTasks(name="英语", next_begin_time=datetime.datetime.today().date(),
                       progress=10)
    db.session.add_all([item1, item2, item3])
    db.session.commit()


def add_new_learned():
    in_date = '2021-07-28'
    dt = datetime.datetime.strptime(in_date, "%Y-%m-%d")
   # out_date = (dt + datetime.timedelta(days=2)).strftime("%Y-%m-%d")

    item1 = DailyTasks(total_task_id=1, name="语文第8.1章",
                       next_begin_time=dt, progress=10)
    item2 = DailyTasks(total_task_id=2, name="数学第8.1章",
                       next_begin_time=dt, progress=10)
    item3 = DailyTasks(total_task_id=3, name="英语第8.1章",
                       next_begin_time=dt, progress=10)
    db.session.add_all([item1, item2, item3])
    db.session.commit()


def delete_items(table_class):
    t = table_class.query.all()
    for i in t:
        db.session.delete(i)
        db.session.commit()


if __name__ == '__main__':
    # delete_items(DailyTasks)
    add_total_tasks()
