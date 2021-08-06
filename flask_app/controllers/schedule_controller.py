from flask_app.models.schedule import Schedule
from flask_app import app
from flask import render_template, redirect, request, session, flash
# from flask_app.models.schedule import Schedule
from flask_app.models.user import User

@app.route('/landing')
def landing():
    if "user_id" not in session:
        return redirect('/')
    users = {
        'id': session['user_id']
    }
    user = User.user_info(users)
    user_schedules = Schedule.show_shift(users)

    return render_template('index.html', user=user[0], schedules = user_schedules, day_off=Schedule.day_off)