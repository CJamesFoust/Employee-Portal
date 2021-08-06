from flask import Flask, flash
from flask_app.config.mysqlconnection import connectToMySQL

class Pto:
    def __init__(self,data):
        self.id = data['id']
        self.begin_date_request = data['begin_date_request']
        self.end_date_request = data["end_date_request"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        if 'user' in data:
            self.user = data['user']

    @classmethod
    def request_pto(cls,data):
        query = "INSERT INTO pto_requests(user_id, begin_date_request, end_date_request, created_at, updated_at, reason) VALUES(%(user_id)s, %(begin_date_request)s, %(end_date_request)s, NOW(), NOW(), %(reason)s);"
        pto_id = connectToMySQL('employee_portal').query_db(query,data)

        return pto_id


    @classmethod
    def get_request(cls, data):
        return connectToMySQL("employee_portal").query_db("SELECT * FROM pto_requests WHERE user_id = %(id)s;",data)


    @classmethod
    def get_request_by_id(cls, data):
        return connectToMySQL("employee_portal").query_db("SELECT * FROM pto_requests WHERE id = %(id)s;",data)


    @classmethod
    def delete_request(cls, data):
        return connectToMySQL("employee_portal").query_db("DELETE FROM pto_requests WHERE id = %(id)s;",data)


    @classmethod
    def update_request(cls, data):
        query = "UPDATE pto_requests SET begin_date_request = %(begin_date_request)s, end_date_request = %(end_date_request)s, reason = %(reason)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL("employee_portal").query_db(query, data)

    @staticmethod
    def validate_pto(data):
        is_valid = True
        if len(data['begin']) < 3:
            flash("Please enter valid start date", "pto")
            is_valid = False
        if len(data['end']) < 3:
            flash('Please enter valid end date', "pto")
            is_valid = False
        if len(data['reason']) < 3:
            flash('Reason must contain at least 3 characters', "pto")
            is_valid = False
        
        return is_valid
