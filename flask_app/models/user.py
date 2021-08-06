from flask import Flask, flash
from flask_bcrypt import Bcrypt
from flask_app import app
from flask_app.config.mysqlconnection import connectToMySQL
import re
from datetime import date
from ..models import schedule

bcrypt = Bcrypt(app)



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASS_REGEX = re.compile('^(?=\S{8,30}$)(?=.*?\d)(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^A-Za-z\s0-9])')

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.schedules = []
        self.pto_requests = []


    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users LEFT JOIN schedules ON users.id = schedules.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL("employee_portal").query_db(query,data)

        user = cls(results[0])
        if results[0]['schedules.id'] != None:
            for row in results:
                row_data = {
                    'id': row['shows.id'],
                    'work_date': row['work_date'],
                    'start_work_hour': row['start_work_hour'],
                    'end_work_hour': row['end_work_hour'],
                    'created_at': row['shows.created_at'],
                    'updated_at': row ['shows.updated_at'],
                }
                user.schedules.append(schedule.Shedule(row_data))
        
        return user


    @classmethod
    def create_user(cls, data):
        return connectToMySQL('employee_portal').query_db("INSERT INTO users (first_name,last_name,email,password,created_at,updated_at) "\
            "VALUES(%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());", data)

    @classmethod
    def update_user(cls,data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s, updated_at = NOW() WHERE id = %(id)s;"
        user_id = connectToMySQL("employee_portal").query_db(query,data)

        return user_id

    @classmethod
    def check_email(cls, data):
        count = connectToMySQL('employee_portal').query_db("SELECT count(*) FROM users WHERE users.email = %(email)s;", data)
        count = [ key['count(*)'] for key in count]
        if count[0] == 0:
            return False
        else:
            return True


    @classmethod
    def check_login_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("employee_portal").query_db(query, data)
        if len(result) < 1:
            return False
        return cls(result[0])


    @staticmethod
    def validate(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.", 'first_name')
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters.", 'last_name')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", 'email')
            is_valid = False
        if EMAIL_REGEX.match(data['email']):
            if User.check_email(data):
                flash("This email is already registered", 'email')
                is_valid = False
        if not PASS_REGEX.match(data['password']):
            flash('Check that password meets requirements.', 'password')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords must match.", 'confirm')
            is_valid = False
        
        return is_valid

    @classmethod
    def user_info(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("employee_portal").query_db(query, data)
        return result

    @staticmethod
    def update_validate(data):
        is_valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.", 'first_name')
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters.", 'last_name')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!", 'email')
            is_valid = False
        if not PASS_REGEX.match(data['password']):
            flash('Check that password meets requirements.', 'password')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords must match.", 'confirm')
            is_valid = False
        return is_valid