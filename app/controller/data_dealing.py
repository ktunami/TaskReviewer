# python3
# _*_ coding: utf-8 _*_
# @Time  : 2021/7/27
# @Author: Kate
# @File  : data_dealing.py


from app import app, db
from app.model.common_checks import *
from app.model.daily_tasks import DailyTasks
from app.model.today_work import TodayWork
from app.model.total_tasks import TotalTasks
from app.model.total_done import TotalDone
from app.model.long_term_items import LongTermItems
from app.model.recent_items import RecentItems


def review_dealing(val):
    """
    :param val: Id of DailyTasks
    Update DailyTasks by review information
    """
    item = DailyTasks.query.filter_by(id=val).first()
    new_learned_times = item.learned_times + 1
    review_interval = app.config.get("REVIEW_RULES")[new_learned_times]
    new_next_begin_time = (
            datetime.datetime.today().date() + datetime.timedelta(days=review_interval))
    DailyTasks.query.filter_by(id=val).update({'learned_times': new_learned_times,
                                               'next_begin_time': new_next_begin_time})
    db.session.commit()


def add_new_short_items(result):
    all_names = result.getlist("name")
    all_contents = result.getlist("content")
    all_remarks = result.getlist("remarks")
    all_need_days = result.getlist("need_days")
    li = []
    for i in range(len(all_names)):
        item = RecentItems(name=all_names[i],
                    content=all_contents[i],
                    is_content_link=check_is_url(all_contents[i]),
                    remarks=all_remarks[i],
                    expected_days=all_need_days[i])
        li.append(item)
    if len(li):
        db.session.add_all(li)
        db.session.commit()


def add_new_long_items(result):
    all_names = result.getlist("name")
    all_contents = result.getlist("content")
    all_remarks = result.getlist("remarks")
    all_expect_begins = result.getlist("expect_begin")
    all_expect_ends = result.getlist("expect_end")
    data_size = len(all_names)
    li = []
    for i in range(data_size):
        item = LongTermItems(name=all_names[i],
                             content=all_contents[i],
                             is_content_link=check_is_url(all_contents[i]),
                             remarks=all_remarks[i],
                             expected_begin_time=all_expect_begins[i],
                             expected_end_time=all_expect_ends[i])
        li.append(item)
    if len(li):
        db.session.add_all(li)
        db.session.commit()


def update_new_short_items(result):
    all_name = result.getlist("name")
    all_id = result.getlist("item_id")
    all_content = result.getlist("content")
    all_remarks = result.getlist("remarks")
    all_need_days = result.getlist("need_days")
    all_end_checkbox = result.getlist("is_end")
    for i in range(len(all_name)):
        RecentItems.query.filter_by(id=all_id[i]).update({
            'name': all_name[i],
            'content': all_content[i],
            'is_content_link': check_is_url(all_content[i]),
            'remarks': all_remarks[i],
            'expected_days': get_days(all_need_days[i]),
        })
    for i in all_end_checkbox:
        RecentItems.query.filter_by(id=i).update({'already_complete': True})
    db.session.commit()


def update_long_items(result):
    all_name = result.getlist("name")
    all_id = result.getlist("item_id")
    all_content = result.getlist("content")
    all_remarks = result.getlist("remarks")
    all_start_time = result.getlist("s_time")
    all_end_time = result.getlist("e_time")
    all_start_checkbox = result.getlist("is_begin")
    all_end_checkbox = result.getlist("is_end")
    for i in range(len(all_name)):
        print("id is  ", all_id[i])
        LongTermItems.query.filter_by(id=all_id[i]).update({
                'name': all_name[i],
                'content':all_content[i],
                'is_content_link':check_is_url(all_content[i]),
                'remarks':all_remarks[i],
                'expected_begin_time':get_date(all_start_time[i]),
                'expected_end_time':get_date(all_end_time[i])
        })
    for i in all_start_checkbox:
        LongTermItems.query.filter_by(id=i).update({'already_begin':True})
    for i in all_end_checkbox:
        LongTermItems.query.filter_by(id=i).update({'already_complete':True})
    db.session.commit()


def new_learned_dealing(result):
    """
    :param result: New learned stuff
    Deal with new learned stuff, insert them into table 'today_work'
    """
    total_task_ids = result.getlist("total_task_id")
    other_total_task_names = result.getlist("other_total_task_name")
    sub_task_names = result.getlist("sub_task_name")
    prog = result.getlist("progress")
    data_size = len(total_task_ids)
    li = []
    for i in range(data_size):
        item = TodayWork(total_task_id=total_task_ids[i],
                         total_task_name=other_total_task_names[i],
                         name=sub_task_names[i],
                         progress=prog[i])
        li.append(item)
    if len(li):
        db.session.add_all(li)
        db.session.commit()


def update_db_by_new_stuff(ids):
    new_ids = ids.getlist("new_reviewed")
    for i in new_ids:
        total_line = TodayWork.query.filter(TodayWork.id == i).first()
        new_date = total_line.today_date + datetime.timedelta(days=app.config.get('REVIEW_RULES')[1])
        if total_line.total_task_id == 0:
            item = TotalTasks(name=total_line.total_task_name, next_begin_time=total_line.today_date,
                              progress=total_line.progress)
            db.session.add(item)
            new_total_insert = TotalTasks.query.filter(TotalTasks.name == total_line.total_task_name).first()
            item_d = DailyTasks(total_task_id=new_total_insert.id, name=total_line.name,
                                next_begin_time=new_date, progress=total_line.progress)
            db.session.add(item_d)
            db.session.commit()
        else:
            item_d = DailyTasks(total_task_id=total_line.total_task_id, name=total_line.name,
                                next_begin_time=new_date, progress=total_line.progress)
            db.session.add(item_d)
            total_to_be_updated = TotalTasks.query.filter(TotalTasks.id == total_line.total_task_id).first()
            new_progress = total_to_be_updated.progress + total_line.progress
            TotalTasks.query.filter_by(
                id=total_line.total_task_id).update({'progress': new_progress,
                                                     'next_begin_time': total_line.today_date})
            db.session.commit()
        db.session.delete(total_line)
        db.session.commit()


def pre_dealing():
    records = TotalTasks.query.filter(TotalTasks.progress >= 100).all()
    for rec in records:
        learned_times = rec.learned_times + 1
        if learned_times > len(app.config.get('TOTAL_REVIEW_RULES')):
            new_item = TotalDone(name=rec.name, learned_times=rec.learned_times,
                                 last_time=rec.next_begin_time)
            db.session.add(new_item)
            db.session.delete(rec)
            db.session.commit()
        else:
            next_date = rec.next_begin_time + datetime.timedelta(
                days=app.config.get('TOTAL_REVIEW_RULES')[learned_times])
            TotalTasks.query.filter_by(id=rec.id).update({'learned_times': learned_times,
                                                          'next_begin_time': next_date,
                                                          'progress': 0})
            db.session.commit()
