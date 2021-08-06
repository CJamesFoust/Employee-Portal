from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.pto import Pto



@app.route('/pto')
def PTO():
    if "user_id" not in session:
        return redirect('/')
    users = {
        'id': session['user_id']
    }
    user = User.user_info(users)
    requests = Pto.get_request(users)
    return render_template('pto.html', user=user[0], requests=requests)


@app.route('/submit-request', methods=['POST'])
def submit_request():
    if "user_id" not in session:
        return redirect('/')
    if not Pto.validate_pto(request.form):
        return redirect('/pto')
    data = {
        'begin_date_request': request.form['begin'],
        'end_date_request': request.form['end'],
        'user_id': session['user_id'],
        'reason': request.form['reason']
    }
    Pto.request_pto(data)
    return redirect('/pto')


@app.route('/edit-request', methods=['POST'])
def edit_request():
    if not Pto.validate_pto(request.form):
        return redirect('/')
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id': request.form['id'],
        'begin_date_request': request.form['begin'],
        'end_date_request': request.form['end'],
        'reason': request.form['reason'],        
    }
    Pto.update_request(data)
    return redirect('/pto')


@app.route('/delete/<int:request_id>')
def delete_request_(request_id):
    if "user_id" not in session:
        return redirect('/')
    data = {
        'id': request_id
    }
    Pto.delete_request(data)
    return redirect('/pto')


@app.route('/edit/<int:request_id>')
def edit_request_(request_id):
    data = {
        'id': request_id
    }
    if "user_id" not in session:
        return redirect('/')
    users = {
        'id': session['user_id']
    }
    user = User.user_info(users)
    request = Pto.get_request_by_id(data)
    return render_template('pto_edit.html', user=user[0], request=request[0])