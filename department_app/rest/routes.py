from datetime import datetime

from flask import request
from flask_restful import Resource
from sqlalchemy import func

from department_app import app
from department_app.service.factories import *
from department_app.models.models import Departments, Employee
from department_app import db


class EmployeeCRUD(Resource):
    """
    REST Employee CRUD operations with DB
    """
    def get(self):
        """
        READ operation with DB for Employee table

        :return: employee list, 200 status code
        """
        employee_list = db.session.query(Employee).all()
        employee_list = [

                [
                        employee.employee_id,
                        employee.employee_name,
                        employee.date_of_birth.isoformat(),
                        employee.department.department_name,
                ]
                for employee in employee_list
                ]

        return {'data': employee_list}, 200

    def post(self):
        """
        CREATE operation with DB for Employee table

        :return: employee list, 200 status code
        """
        pass
        """pets = db.session.query(Pets.room_num, func.count(Pets.room_num)). \
            group_by(Pets.room_num).all()
        filled_rooms = set([pet.room_num for pet in pets])
        empty_rooms = set(range(1, 21))
        empty_rooms -= filled_rooms

        return {'empty rooms': list(empty_rooms)}, 200"""

    def put(self):
        """
        UPDATE operation with DB for Employee table

        :return: employee list, 200 status code
        """
        pass
        """pets = db.session.query(Pets.room_num, func.count(Pets.room_num)). \
            group_by(Pets.room_num).all()
        filled_rooms = set([pet.room_num for pet in pets])
        empty_rooms = set(range(1, 21))
        empty_rooms -= filled_rooms

        return {'empty rooms': list(empty_rooms)}, 200"""

    def delete(self):
        """
        DELETE operation with DB for Employee table

        :return: employee list, 200 status code
        """
        pass
        """pets = db.session.query(Pets.room_num, func.count(Pets.room_num)). \
            group_by(Pets.room_num).all()
        filled_rooms = set([pet.room_num for pet in pets])
        empty_rooms = set(range(1, 21))
        empty_rooms -= filled_rooms

        return {'empty rooms': list(empty_rooms)}, 200
"""


class DepartmentsCRUD(Resource):
    """
    REST Departments CRUD operations with DB
    """
    def get(self):
        pass
        """activities = db.session.query(Pets, Activities).all()
        result = []
        for activity in activities:
            result.append(
                    {
                            "pet_name": activity[0].pet_name,
                            "day": activity[1].activity_time.day,
                            "hour": activity[1].activity_time.hour,
                            "minute": activity[1].activity_time.minute,
                            "type": activity[1].activity_type
                            }
                    )
        print(result)
        return {'Activities': result}, 200"""


class TestDBData(Resource):
    """
    REST creating of test data in DB
    """
    def post(self):
        """
        CREATE operation with DB for Departments and Employee tables

        :return: "Successfully created test data", 200 status code
        """
        for i in range(10):
            department = DepartmentFactory.create()
            employee = EmployeeFactory.create_batch(
                    10,
                    department_id=department.department_id)
        db.session.commit()

        return "Successfully created test data", 200

    def delete(self):
        """
        DELETE operation with DB for Departments and Employee tables

        :return: "Successfully deleted all data in DB", 200 status code
        """
        Employee.query.delete()
        Departments.query.delete()
        db.session.commit()

        return "Successfully deleted all data in DB", 200
