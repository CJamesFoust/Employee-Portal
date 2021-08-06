from flask import Flask, flash
from flask_bcrypt import Bcrypt
from flask_app.config.mysqlconnection import connectToMySQL
import re

from flask_app import app
from ..models import user

class Schedule:
    def __init__(self,data):
        self.id = data['id']
        self.work_date = data['work_date']
        self.start_work_hour = data["start_work_hour"]
        self.end_work_hour = data["end_work_hour"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        if 'user' in data:
            self.user = data['user']

    @classmethod
    def show_schedule(cls):
        query = "SELECT * FROM schedules;"
        schedules_from_db = connectToMySQL('employee_portal').query_db(query)
        schedules = []
        for schedule in schedules_from_db:
            schedules.append(cls(schedule))
        return schedules 


    @classmethod 
    def show_shift(cls,data):
        query = "SELECT * FROM schedules WHERE employee_id = %(id)s;"
        results = connectToMySQL("employee_portal").query_db(query,data)
        return results


    @classmethod
    def day_off(cls, data):
        if data is None:
            return "Day Off"
        else:
            return data.strftime('%I:%M %p')