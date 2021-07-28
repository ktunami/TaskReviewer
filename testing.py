from app import db
from app.model.total_tasks import TotalTasks
from app.model.daily_tasks import DailyTasks
import datetime

def get_date(str):
    return datetime.datetime.strptime(str, "%Y-%m-%d")


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
    # delete_items(DailyTasks)
    add_total_tasks()
