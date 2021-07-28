from flask import Flask, render_template, request, redirect, url_for
from app.model.total_tasks import TotalTasks
from app.model.today_work import TodayWork
from sqlalchemy import and_
from app.controller.data_deeling import *


@app.route('/', methods=['POST', 'GET'])
def index():
    current_date = datetime.datetime.today().date()
    pre_deeling()
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
        DailyTasks.last_time, DailyTasks.next_begin_time
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
            review_deeling(val)
        return redirect(url_for('index'))


@app.route('/new_learn', methods=['POST'])
def new_learn_process():
    if request.method == 'POST':
        result = request.form
        new_learned_deeling(result)
        return redirect(url_for('index'))

@app.route('/insert_new_stuff', methods=['POST'])
def new_learn_for_review():
    if request.method == 'POST':
        result = request.form
        update_db_by_new_stuff(result)
        return redirect(url_for('index'))
