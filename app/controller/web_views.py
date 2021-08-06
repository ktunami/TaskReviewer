# python3
# _*_ coding: utf-8 _*_
# @Time  : 2021/7/27
# @Author: Kate
# @File  : web_views.py

from flask import render_template, request, redirect, url_for
from sqlalchemy import and_
from app.controller.data_dealing import *
from app.model.long_term_items import LongTermItems


@app.route('/', methods=['POST', 'GET'])
def index():
    current_date = datetime.datetime.today().date()
    pre_dealing()
    all_tasks = TotalTasks.query.all()
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
        daily_ids = request.form.getlist("reviewed")
        for val in daily_ids:
            review_dealing(val)
        return redirect(url_for('index'))


@app.route('/new_learn', methods=['POST'])
def new_learn_process():
    if request.method == 'POST':
        result = request.form
        new_learned_dealing(result)
        return redirect(url_for('index'))


@app.route('/insert_new_stuff', methods=['POST'])
def new_learn_for_review():
    if request.method == 'POST':
        result = request.form
        update_db_by_new_stuff(result)
        return redirect(url_for('index'))


@app.route('/my_tasks', methods=['POST', 'GET'])
def my_tasks():
    l_term_tasks = LongTermItems.query.filter(LongTermItems.already_complete==False).all()
    s_term_tasks = RecentItems.query.filter(RecentItems.already_complete == False).all()
    return render_template('my_tasks.html',
                           l_term_tasks=l_term_tasks,
                           s_term_tasks=s_term_tasks,
                           date=datetime.datetime.today().date(),
                           week_day=app.config.get('WEEKDAYS_DISPLAY')[datetime.date.today().weekday()]
                           )


@app.route('/already_done', methods=['GET'])
def already_done():
    if request.method == 'GET':
        return render_template('already_done.html',
                               date=datetime.datetime.today().date(),
                               week_day=app.config.get('WEEKDAYS_DISPLAY')[datetime.date.today().weekday()]
                               )


@app.route('/deal_short_items', methods=['POST'])
def deal_short_items():
    result = request.form
    update_new_short_items(result)
    return redirect(url_for('my_tasks'))


@app.route('/add_short_items', methods=['POST'])
def add_short_items():
    result = request.form
    add_new_short_items(result)
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