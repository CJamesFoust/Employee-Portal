from flask.helpers import url_for
from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from ..models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)




@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/landing')
    return render_template('login.html')


@app.route('/create', methods=['POST'])
def create():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
    }
    if User.validate(request.form) == True:
        data['password'] = bcrypt.generate_password_hash(data['password'])
        session['user_id'] = User.create_user(data)
        return redirect('/landing')
    return redirect('/')

@app.route('/update/<int:id>')
def update(id):
    if "user_id" not in session:
        return redirect('/')
    users = {
        'id': session['user_id']
    }
    user = User.user_info(users)

    return render_template('account.html', user=user[0])

@app.route('/update_account/<int:id>', methods = ['POST'])
def update_show(id):
    if "user_id" not in session:
        return redirect('/') 
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": request.form['password'],
        "id": id
    }
    
    if not User.update_validate(request.form):
        return redirect(f'/update/{id}')
    user = User.user_info(data)
    print(user)
    if not bcrypt.check_password_hash(user[0]['password'], request.form['old_password']):
        flash("Please check that you're entering the correct password", 'old_password')
        return redirect(url_for('.update', id=data['id']))
    data['password'] = bcrypt.generate_password_hash(data['password'])                    
    User.update_user(data)
    flash("Information successfully updated", "success")
    return redirect(url_for('.update', id=data['id']))

@app.route('/login', methods=['POST'])
def login():
    data = {
        'email': request.form['email']
    }
    user_in_db = User.check_login_email(data)
    if not user_in_db:
        flash("Login Failed: Email not in system, or password doesn't match", 'login_failed')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Login Failed: Email not in system, or password doesn't match", 'login_failed')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['attempt'] = 0
    return redirect('/landing')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
