# python3
# _*_ coding: utf-8 _*_
# @Time  : 2021/7/27
# @Author: Kate
# @File  : web_views.py

from flask import render_template, request, redirect, url_for
from app.controller.data_dealing import *
from app.model.long_term_items import LongTermItems
import json
import time


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    if fmt is None:
        fmt = '%H:%M'
    if date is None:
        return '--'
    else:
        return date.strftime(fmt)


@app.route('/', methods=['POST', 'GET'])
def index():
    current_date = datetime.datetime.today().date()
    pre_dealing()
    all_tasks = TotalTasks.query.all()
    all_tasks.sort(key=lambda item: item.learned_times)
    today_learned = TodayWork.query.all()
    for learn_item in today_learned:
        if learn_item.total_task_id:
            total_line = TotalTasks.query.filter(
                TotalTasks.id == learn_item.total_task_id).first()
            learn_item.total_task_name = total_line.name
    all_need_reviews = db.session.query(
        TotalTasks.id, DailyTasks.total_task_id, DailyTasks.id.label("id"),
        TotalTasks.name.label("t_name"), DailyTasks.name, DailyTasks.learned_times,
        DailyTasks.next_begin_time
    ).filter(and_(DailyTasks.next_begin_time <= current_date,
                  DailyTasks.learned_times < len(app.config.get('REVIEW_RULES')))). \
        filter(TotalTasks.id == DailyTasks.total_task_id).all()
    review_yesterday = [item for item in all_need_reviews
                        if (item.learned_times == 0 and item.next_begin_time == current_date)]
    other_need_review = [item for item in all_need_reviews if item not in review_yesterday]
    return render_template("index.html",
                           all_tasks=all_tasks,
                           today_learned=today_learned,
                           review_yesterday=review_yesterday,
                           other_need_review=other_need_review,
                           date=datetime.datetime.today().date(),
                           week_day=app.config.get('WEEKDAYS_DISPLAY')[datetime.date.today().weekday()])


@app.route('/review', methods=['POST'])
def review_process():
    if request.method == 'POST':
        change_names(request.form, 2)
        daily_ids = request.form.getlist("reviewed")
        for val in daily_ids:
            review_dealing(val)
        return redirect(url_for('index'))


@app.route('/new_learn', methods=['POST'])
def new_learn_process():
    if request.method == 'POST':
        result = request.form
        change_names(result, 1)
        current_date = datetime.datetime.today().date()
        new_learned_dealing(result, current_date)
        return redirect(url_for('index'))


@app.route('/insert_new_stuff', methods=['POST'])
def new_learn_for_review():
    if request.method == 'POST':
        result = request.form
        change_names(result, 2)
        update_db_by_new_stuff(result)
        return redirect(url_for('index'))


@app.route('/change_t_name', methods=['POST', 'GET'])
def change_t_name():
    result = request.form
    change_names(result, 0)
    return redirect(url_for('index'))


@app.route('/my_tasks', methods=['POST', 'GET'])
def my_tasks():
    start_time = time.time()
    wd = app.config.get('WEEKDAYS_DISPLAY')[datetime.date.today().weekday()]
    today_date = datetime.datetime.today().date()
    pre_dealing()
    l_term_tasks = LongTermItems.query.filter(LongTermItems.already_complete == False). \
        order_by(LongTermItems.already_begin.desc()). \
        order_by(LongTermItems.done_times.asc()). \
        order_by(LongTermItems.expected_end_time.asc()). \
        order_by(LongTermItems.id.asc()).all()
    s_term_data1 = RecentItems.query.filter(
        and_(RecentItems.already_complete == False, today_date >= RecentItems.create_date)
        ).filter(RecentItems.expected_days < 0). \
        order_by(RecentItems.start_time.asc()).all()
    s_term_data2 = RecentItems.query.filter(
        RecentItems.already_complete == False).filter(RecentItems.expected_days >= 0).all()
    s_term_data2.sort(key=lambda item: item.create_date + datetime.timedelta(days=item.expected_days))
    s_term_data1.extend(s_term_data2)
    s_term_li = []
    for item in s_term_data1:
        if is_short_item_available(today_date, item.create_date, item.expected_days):
            s_term_li.append(item)
    end_time = time.time()
    print("time:%f" % (end_time - start_time))
    return render_template('my_tasks.html',
                           s_term_tasks=s_term_li,
                           l_term_tasks=l_term_tasks,
                           date=today_date,
                           week_day=wd,
                           categories=app.config.get('CATEGORIES')
                           )


@app.route('/already_done', methods=['GET'])
def already_done():
    all_projects_done = LongProjectsDone.query.all()
    print(all_projects_done)
    if request.method == 'GET':
        return render_template('already_done.html',
                               all_projects_done=all_projects_done,
                               date=datetime.datetime.today().date(),
                               week_day=app.config.get('WEEKDAYS_DISPLAY')[datetime.date.today().weekday()]
                               )


# TODO 1
@app.route('/all_expense', methods=['GET', 'POST'])
def all_expense():
    cates = app.config.get('SHOPPING_CATEGORIES')
    if request.method == 'GET':
        return render_template('expense.html',
                               shopping_items=None,
                               main_cate=None,
                               sub_cate=None,
                               dates=None,
                               all_money=None,
                               st_json=None,
                               categories=json.dumps(cates),
                               cate_list=cates.keys(),
                               date=datetime.datetime.today().date(),
                               week_day=app.config.get('WEEKDAYS_DISPLAY')[datetime.date.today().weekday()]
                               )
    else:
        result = request.form
        items, main_cate, sub_cate, dates, all_money, st_json = get_shopping_items(result)
        return render_template('expense.html',
                               shopping_items=items,
                               main_cate=main_cate,
                               sub_cate=sub_cate,
                               dates=dates,
                               all_money=all_money,
                               st_json=st_json,
                               categories=json.dumps(cates),
                               cate_list=cates.keys(),
                               date=datetime.datetime.today().date(),
                               week_day=app.config.get('WEEKDAYS_DISPLAY')[datetime.date.today().weekday()]
                               )


@app.route('/add_shopping', methods=['POST'])
def add_shopping():
    result = request.form
    add_new_expense(result)
    return redirect(url_for('all_expense'))


@app.route('/deal_short_items', methods=['POST'])
def deal_short_items():
    result = request.form
    update_new_short_items(result)
    return redirect(url_for('my_tasks'))


@app.route('/add_short_items', methods=['POST'])
def add_short_items():
    result = request.form
    current_date = datetime.datetime.today().date()
    add_new_short_items(result, current_date)
    return redirect(url_for('my_tasks'))


@app.route('/deal_long_items', methods=['POST'])
def deal_long_items():
    result = request.form
    update_long_items(result)
    return redirect(url_for('my_tasks'))


@app.route('/add_long_items', methods=['POST'])
def add_long_items():
    result = request.form
    add_new_long_items(result)
    return redirect(url_for('my_tasks'))


@app.route('/deal_tips', methods=['POST', 'GET'])
def deal_tips():
    if request.method == 'GET':
        tip_id = request.args.get("id")
        del_tip = TipsRecord.query.filter_by(id=int(tip_id)).first()
        db.session.delete(del_tip)
        db.session.commit()
    else:
        result = request.form
        update_tips(result)
    return redirect(url_for('tips_page'))


@app.route('/add_tips', methods=['POST'])
def add_tips():
    result = request.form
    add_new_tips(result)
    return redirect(url_for('tips_page'))


@app.route('/tips_page', methods=['POST', 'GET'])
def tips_page():
    today_date = datetime.datetime.today().date()
    tips = get_all_tips_and_links()
    return render_template('tips.html',
                           tips=tips,
                           date=today_date,
                           week_day=app.config.get('WEEKDAYS_DISPLAY')[datetime.date.today().weekday()]
                           )
