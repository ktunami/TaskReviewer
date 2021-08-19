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
from app.model.long_term_items import LongTermItems
from app.model.recent_items import RecentItems
from app.model.long_projects_done import LongProjectsDone
from app.model.links_record import LinksRecord
from app.model.tips_record import TipsRecord
from sqlalchemy import and_


def review_dealing(val):
    """
    Update DailyTasks by review information
    :param val: Id of DailyTasks
    """
    item = DailyTasks.query.filter_by(id=val).first()
    new_learned_times = item.learned_times + 1
    review_interval = app.config.get("REVIEW_RULES")[new_learned_times]
    new_next_begin_time = (
            datetime.datetime.today().date() + datetime.timedelta(days=review_interval))
    DailyTasks.query.filter_by(id=val).update({'learned_times': new_learned_times,
                                               'next_begin_time': new_next_begin_time})
    db.session.commit()


def add_new_short_items(result, current_date):
    """
    Add tasks to table 'recent_items'
    :param result: New recent tasks
    """
    all_names = result.getlist("name")
    all_contents = result.getlist("content")
    all_remarks = result.getlist("remarks")
    all_need_days = result.getlist("need_days")
    all_start_times = result.getlist("start_time")
    all_end_times = result.getlist("end_time")
    li = []
    for i in range(len(all_names)):
        item = RecentItems(name=all_names[i],
                           content=all_contents[i],
                           is_content_link=check_is_url(all_contents[i]),
                           remarks=all_remarks[i],
                           expected_days=all_need_days[i],
                           create_date=current_date,
                           start_time=get_checked_time(all_start_times[i]),
                           end_time=get_checked_time(all_end_times[i]))
        li.append(item)
    if len(li):
        db.session.add_all(li)
        db.session.commit()


def add_new_long_items(result):
    """
    Add projects to table 'long_term_items'
    :param result: New projects
    """
    all_names = result.getlist("name")
    all_categories = result.getlist("category")
    all_contents = result.getlist("content")
    all_remarks = result.getlist("remarks")
    all_expect_begins = result.getlist("expect_begin")
    all_expect_ends = result.getlist("expect_end")
    data_size = len(all_names)
    li = []
    for i in range(data_size):
        item = LongTermItems(name=all_names[i],
                             category=all_categories[i],
                             content=all_contents[i],
                             is_content_link=check_is_url(all_contents[i]),
                             remarks=all_remarks[i],
                             expected_begin_time=all_expect_begins[i],
                             expected_end_time=all_expect_ends[i])
        li.append(item)
    if len(li):
        db.session.add_all(li)
        db.session.commit()


def add_new_tips(result):
    """
    Add new tips to table 'tips_record' and 'links_record'
    :param result: New tips
    """
    all_names = result.getlist("name")
    all_instruction = result.getlist("instruction")
    all_content = result.getlist("content")
    all_remarks = result.getlist("remarks")
    tip = TipsRecord(name=all_names[0], instruction=all_instruction[0])
    db.session.add(tip)
    db.session.commit()
    li = []
    for i in range(len(all_content)):
        if all_content[i] != "" or all_remarks[i] != "":
            li.append(LinksRecord(tip_id=tip.id, content=all_content[i], remarks=all_remarks[i]))
    db.session.add_all(li)
    db.session.commit()


def get_all_tips_and_links():
    """
    Get all records from table 'tips_record' and 'links_record'
    :return: Lists of tips and links
    """
    tips = TipsRecord.query.all();
    links = LinksRecord.query.all();
    result = []
    id_map = {}
    for i in range(len(tips)):
        result.append([tips[i], []])
        id_map[tips[i].id] = i
    for j in range(len(links)):
        idx = id_map[links[j].tip_id]
        result[idx][1].append(links[j])
    return result


def update_tips(result):
    all_tip_ids = result.getlist("tip_id")
    all_link_ids = result.getlist("link_id")
    all_names = result.getlist("name")
    all_instruction = result.getlist("instruction")
    all_content = result.getlist("content")
    all_remarks = result.getlist("remarks")
    all_need_delete = result.getlist("del_link")
    all_content_new = result.getlist("content_new")
    all_remarks_new = result.getlist("remarks_new")
    # Update tips_record
    TipsRecord.query.filter_by(id=int(all_tip_ids[0])).update({
        'name': all_names[0],
        'instruction': all_instruction[0]
    })
    # Update links_record
    for j in range(len(all_link_ids)):
        if all_link_ids[j] in all_need_delete:
            del_link = LinksRecord.query.filter_by(id=int(all_link_ids[j])).first()
            db.session.delete(del_link)
        elif all_content[j] != "" or all_remarks[j] != "":
            LinksRecord.query.filter_by(id=int(all_link_ids[j])).update({
                'content': all_content[j],
                'remarks': all_remarks[j]
            })
        else:
            del_link = LinksRecord.query.filter_by(id=int(all_link_ids[j])).first()
            db.session.delete(del_link)
    # Add new items to links_record
    links_li = []
    print(all_remarks_new)
    for k in range(len(all_content_new)):
        if all_content_new[k] != "" or all_remarks_new[k] != "":
            links_li.append(LinksRecord(
                tip_id=all_tip_ids[0],
                content=all_content_new[k],
                remarks=all_remarks_new[k]
            ))
    db.session.add_all(links_li)
    db.session.commit()


def update_new_short_items(result):
    """
    Update tasks in table 'recent_items'
    :param result: Modified recent tasks
    """
    all_name = result.getlist("name")
    all_id = result.getlist("item_id")
    all_content = result.getlist("content")
    all_remarks = result.getlist("remarks")
    all_need_days = result.getlist("need_days")
    all_end_checkbox = result.getlist("is_end")
    all_start_times = result.getlist("start_time")
    all_end_times = result.getlist("end_time")
    current_date = datetime.datetime.today().date()
    all_create_times = result.getlist("create_time")
    all_total_ids = result.getlist("total_id")

    id_list = []
    id_name_map = {}
    items = TotalTasks.query.all()
    for each in items:
        id_list.append(each.id)
        id_name_map[each.id] = each.name

    for i in range(len(all_name)):
        RecentItems.query.filter_by(id=all_id[i]).update({
            'name': all_name[i],
            'content': all_content[i],
            'is_content_link': check_is_url(all_content[i]),
            'remarks': all_remarks[i],
            'create_date': get_date(all_create_times[i]),
            'expected_days': get_num(all_need_days[i], 1),
            'already_complete': all_id[i] in all_end_checkbox,
            'start_time': get_checked_time(all_start_times[i]),
            'end_time': get_checked_time(all_end_times[i])
        })
        if all_id[i] in all_end_checkbox:
            RecentItems.query.filter_by(id=i).update({'complete_date': current_date})
            if int(all_total_ids[i]) in id_list:
                name_progress = all_remarks[i].split('_')
                if len(name_progress) == 2:
                    it = TodayWork(
                        total_task_id=all_total_ids[i],
                        total_task_name=id_name_map[int(all_total_ids[i])],
                        name=name_progress[0],
                        progress=int(name_progress[1]),
                        today_date=current_date)
                    db.session.add(it)
    db.session.commit()


def create_study_task(project_id, project_name):
    item = TotalTasks(
            project_id=project_id,
            name=project_name,
            next_begin_time=datetime.datetime.today().date(),
            progress=0,
            create_time=datetime.datetime.today().date())
    db.session.add(item)
    db.session.commit()


def get_task_name(tsk_id, name):
    left_part = '['
    right_part = ']'
    return left_part + tsk_id + right_part + name


def create_recent_periodic_task(tsk_id, name, content, remarks, start_date, category):
    n_name = get_task_name(tsk_id, name)
    st_time, e_time = app.config.get('CATEGORIES')[category]
    item = RecentItems(
        name=n_name,
        content=content,
        is_content_link=check_is_url(content),
        remarks=remarks,
        expected_days='-1',   #str((start_date - current_date).days + 1),
        create_date=start_date,
        start_time=st_time,
        end_time=e_time,
        lid=tsk_id
    )
    db.session.add(item)
    db.session.commit()


def update_long_items(result):
    """
    Update projects in table 'long_term_items'
    :param result: Modified projects
    """
    all_name = result.getlist("name")
    all_id = result.getlist("item_id")
    all_content = result.getlist("content")
    all_remarks = result.getlist("remarks")
    all_start_time = result.getlist("s_time")
    all_end_time = result.getlist("e_time")
    all_start_checkbox = result.getlist("is_begin")
    all_end_checkbox = result.getlist("is_end")
    all_add_to_study = result.getlist("is_study_item")
    all_categories = result.getlist("category")

    # get study item id
    id_list = set([])
    items1 = TotalTasks.query.all()
    for each in items1:
        id_list.add(each.id)
    # get short task id
    short_id_list = set([])
    items2 = RecentItems.query.all()
    for each in items2:
        short_id_list.add(each.long_tsk_id)
    for i in range(len(all_name)):
        LongTermItems.query.filter_by(id=all_id[i]).update({
            'name': all_name[i],
            'category': all_categories[i],
            'content': all_content[i],
            'is_content_link': check_is_url(all_content[i]),
            'remarks': all_remarks[i],
            'expected_begin_time': get_date(all_start_time[i]),
            'expected_end_time': get_date(all_end_time[i]),
            'already_begin': all_id[i] in all_start_checkbox,
            'already_complete': all_id[i] in all_end_checkbox,
            'add_to_study': all_id[i] in all_add_to_study
        })
        # Create or update study item and periodic task
        if all_id[i] in all_add_to_study:
            # study item
            if int(all_id[i]) in id_list:
                TotalTasks.query.filter_by(id=int(all_id[i])).update({'name': all_name[i]})
            else:
                create_study_task(all_id[i], all_name[i])
            # periodic task
            if int(all_id[i]) in short_id_list:
                st_time, e_time = app.config.get('CATEGORIES')[all_categories[i]]
                RecentItems.query.filter_by(long_tsk_id=int(all_id[i])).\
                    update({'name': get_task_name(all_id[i], all_name[i]),
                            'create_date': get_date(all_start_time[i]).date(),
                            'start_time': st_time,
                            'end_time': e_time})
            else:
                create_recent_periodic_task(
                    all_id[i], all_name[i], all_content[i], all_remarks[i],
                    get_date(all_start_time[i]).date(),
                    all_categories[i])
    db.session.commit()


def new_learned_dealing(result, current_date):
    """
    For new learnt stuff, insert them into table 'today_work' temporarily.
    :param result: New learned stuff
    """
    items = TotalTasks.query.all()
    id_name_map = {}
    for each in items:
        id_name_map[each.id] = each.name
    total_task_ids = result.getlist("total_task_id")
    sub_task_names = result.getlist("sub_task_name")
    prog = result.getlist("progress")
    data_size = len(total_task_ids)
    li = []
    for i in range(data_size):
        item = TodayWork(total_task_id=total_task_ids[i],
                         total_task_name=id_name_map[int(total_task_ids[i])],
                         name=sub_task_names[i],
                         progress=get_num(prog[i], 0),
                         today_date=current_date)
        li.append(item)
    if len(li):
        db.session.add_all(li)
        db.session.commit()


def update_db_by_new_stuff(ids):
    """
    Update the progress and the next_begin_time, then add it to table 'daily_tasks'.
    Finally delete the item from table 'today_work'
    :param ids: New learnt stuff after today's review.
    """
    new_ids = ids.getlist("new_reviewed")
    for i in new_ids:
        total_line = TodayWork.query.filter(TodayWork.id == i).first()
        new_date = total_line.today_date + datetime.timedelta(days=app.config.get('REVIEW_RULES')[1])

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
    """
    Data preprocessing
    """
    # Total task and long items
    records = TotalTasks.query.filter(TotalTasks.progress >= 100).all()
    for rec in records:
        learned_times = rec.learned_times + 1
        LongTermItems.query.filter_by(id=rec.id).update({'done_times': learned_times})
        db.session.commit()
        if learned_times > len(app.config.get('TOTAL_REVIEW_RULES')):
            item_to_move = LongTermItems.query.filter_by(id=rec.id).first()
            item = LongProjectsDone(
                id=rec.id,
                name=item_to_move.name,
                content=item_to_move.content,
                is_content_link=item_to_move.is_content_link,
                remarks=item_to_move.remarks,
                done_time=datetime.datetime.today().date())
            db.session.add(item)
            db.session.delete(item_to_move)
            db.session.delete(rec)
            db.session.commit()
        else:
            next_date = rec.next_begin_time + datetime.timedelta(
                days=app.config.get('TOTAL_REVIEW_RULES')[learned_times])
            TotalTasks.query.filter_by(id=rec.id).update({'learned_times': learned_times,
                                                          'next_begin_time': next_date,
                                                          'progress': 0})
            db.session.commit()
    # Delete canceled projects
    canceled_projects = LongTermItems.query.filter(
        and_(not LongTermItems.already_begin, LongTermItems.already_complete)).all()
    for each in canceled_projects:
        db.session.delete(each)
        db.session.commit()
    # Move finished long projects
    projects_to_be_moved = LongTermItems.query.filter(LongTermItems.already_complete).all()
    li = []
    for each in projects_to_be_moved:
        item = LongProjectsDone(
            id=each.id,
            name=each.name,
            content=each.content,
            is_content_link=each.is_content_link,
            remarks=each.remarks,
            done_time=datetime.datetime.today().date())
        li.append(item)
    db.session.add_all(li)
    for each in projects_to_be_moved:
        db.session.delete(each)
        db.session.commit()
    db.session.commit()
    # Delete finished recent items
    recent_items_to_be_removed = RecentItems.query.filter(
        and_(RecentItems.already_complete, RecentItems.expected_days >= 0)).all()
    for each in recent_items_to_be_removed:
        db.session.delete(each)
        db.session.commit()
    # Deal with completed recent items
    today_date = datetime.datetime.today().date()
    RecentItems.query.filter(RecentItems.complete_date < today_date).update({'already_complete': False})
    db.session.commit()


def is_short_item_available(today_date, create_date, expected_days):
    """
    Check If the current item can be shown
    :param today_date: Today date
    :param create_date: Created date of the short item
    :param expected_days: Days needed
    :return: True if the current item can be shown
    """
    result = True
    if expected_days < 0 and (today_date - create_date).days % abs(expected_days) != 0:
        result = False
    return result


def change_names(result, mode):
    """
    Change names in some tables
    :param result: input data
    :param mode:
          0 ---- total_tasks
          1 ---- today_work
          2 ____ daily_tasks
    """
    all_name = result.getlist("name")
    all_id = result.getlist("id")
    for i in range(len(all_id)):
        if mode == 0:
            TotalTasks.query.filter_by(id=int(all_id[i])).update({'name': all_name[i]})
        elif mode == 1:
            TodayWork.query.filter_by(id=int(all_id[i])).update({'name': all_name[i]})
        else:
            DailyTasks.query.filter_by(id=int(all_id[i])).update({'name': all_name[i]})
        db.session.commit()