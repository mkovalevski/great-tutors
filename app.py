import json
from random import randint, shuffle

from flask import Flask, render_template
from flask_wtf.csrf import CSRFProtect

import dataIntoJSON
from forms import BookingForm, RequestForm, SortForm


app = Flask(__name__)
csrf = CSRFProtect(app)

app.config['SECRET_KEY'] = 'secret_sauce'

data = dataIntoJSON.contents
week = {'mon': 'Понедельник',
        'tue': 'Вторник',
        'wed': 'Среда',
        'thu': 'Четверг',
        'fri': 'Пятница',
        'sat': 'Суббота',
        'sun': 'Воскресенье'}


# соотнести id с преподавателем
def make_new_dict_tutors(data):
    new_dict = {}
    for tutor in data['teachers']:
        new_dict[tutor['id']] = tutor
    return new_dict


# проверка на свободые дни
def count_busy_days(schedule):
    busy_days = {}
    for day, time in schedule.items():
        for isfree in time.values():
            if not isfree:
                busy_days[day] = True
            else:
                busy_days[day] = False
    return busy_days


# добавление записи в booking.json
def add_record_booking(file, name, phone, tutor, day, time):
    new_info = {'name': name, 'phone': phone, 'tutor': tutor, 'day': day, 'time': time}
    with open(file, 'r', encoding='utf-8') as r:
        records = json.load(r)
    records.append(new_info)
    with open(file, 'w', encoding='utf-8') as w:
        json.dump(records, w, ensure_ascii=False)


# добавление записи в request.json
def add_record_request(file, name, phone, purpose, time):
    new_info = {'name': name, 'phone': phone, 'purpose': purpose, 'free_time': time}
    with open(file, 'r', encoding='utf-8') as r:
        records = json.load(r)
    records.append(new_info)
    with open(file, 'w', encoding='utf-8') as w:
        json.dump(records, w, ensure_ascii=False)


# создание словаря только с репетиторами с подходящей целью
def is_goal_in_tutor(goal, tutors):
    tutors_with_goal = []
    for tutor in tutors:
        if goal in tutor['goals']:
            tutors_with_goal.append(tutor)
    return tutors_with_goal


@app.route('/')
def index():
    tutors = make_new_dict_tutors(data)
    rand = []
    random_tutors = {}
    b = 7
    i = 0
    # 6 случайных преподавателей без повторений
    while i <= b:
        if len(rand) == 6:
            break
        random_id = randint(0, 11)
        if random_id not in rand:
            rand.append(random_id)
        else:
            b += 1
        i += 1
    for i in rand:
        random_tutors[i] = tutors[i]
    return render_template('index.html', tutors=random_tutors)


@app.route('/all/',  methods=['GET', 'POST'])
def tutors():
    tutors = make_new_dict_tutors(data)
    shuffle(tutors)
    form = SortForm()
    return render_template('all.html', tutors=tutors, amount=len(tutors), form=form)


@app.route('/all/sort/', methods=['GET', 'POST'])
def sort():
    sort_ids = {
        1: "random",
        2: ["rating", True],
        3: ["price", True],
        4: ["price", False],
    }
    form = SortForm()
    sort_id = form.data['sort']
    sort_attribute = sort_ids[sort_id]
    shuffle(data['teachers'])
    return render_template('all_sort.html', tutors=data['teachers'], amount=len(data['teachers']),
                           form=form, atrs=sort_attribute)


@app.route('/goals/<goal>/')
def goal(goal):
    goals = data['goals']
    emoji = data['emoji']
    tutors_with_goal = is_goal_in_tutor(goal, data['teachers'])
    return render_template('goal.html', goal=goal, goals=goals, emoji=emoji,
                           tutors=tutors_with_goal)


@app.route('/profiles/<int:id>/')
def profile(id):
    tutors = make_new_dict_tutors(data)
    schedule = tutors[id]['free']
    busy_days = count_busy_days(schedule)
    goals = data['goals']
    return render_template('profile.html', id=id, tutors=tutors,
                           week=week, schedule=schedule, goals=goals, busy_days=busy_days)


@app.route('/request/')
def request():
    request_form = RequestForm()
    return render_template('request.html', request_form=request_form)


@app.route('/request_done', methods=['POST'])
def request_done():
    request_form = RequestForm()
    name = request_form.name.data
    phone = request_form.phone.data
    purpose = request_form.purpose.data
    free_time = request_form.free_time.data
    add_record_request('request.json', name, phone, purpose, free_time)
    return render_template('request_done.html', request_form=request_form, name=name, phone=phone,
                           purpose=purpose, free_time=free_time)


@app.route('/booking/<int:id>/<day>/<time>/')
def book(id, day, time):
    tutors = make_new_dict_tutors(data)
    booking_form = BookingForm()
    return render_template('booking.html', id=id, day=week[day], time=time, tutors=tutors,
                           booking_form=booking_form)


@app.route('/booking_done/<tutor>/<day>/<time>', methods=['POST'])
def booking_done(tutor, day, time):
    booking_form = BookingForm()
    name = booking_form.name.data
    phone = booking_form.phone.data
    add_record_booking('booking.json', name, phone, tutor, day, time)
    return render_template('booking_done.html', name=name, phone=phone, tutor=tutor, day=day, time=time)


@app.errorhandler(404)
def not_found(error):
    return "Not Found", 404


# app.run('localhost', port=8000, debug=True)
if __name__ == '__main__':
    app.run()
