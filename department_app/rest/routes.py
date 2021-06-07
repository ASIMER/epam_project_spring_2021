from datetime import datetime
from json import dumps

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
        data = request.args
        # check if we want get only one employee
        if 'employee_id' in data:
            employee_list = db.session.query(Employee).filter_by(
                    employee_id=data['employee_id']
                    ).all()
        else:
            employee_list = db.session.query(Employee).all()
        # error handle for wrong employee id
        if not employee_list and 'employee_id' in data:
            return "No such employee in DB", 404

        employee_list = [

                    {
                        "0": employee.employee_name,
                        "1": employee.date_of_birth.isoformat(),
                        "2": employee.salary,
                        "3": employee.Departments.department_name,
                        "DT_RowId": employee.employee_id
                        }
                    for employee in employee_list
                ]

        return {'data': employee_list}, 200

    def post(self):
        """
        CREATE operation with DB for Employee table

        :return: employee list, 200 status code
        """
        form_data = request.form
        department = db.session.query(Departments).filter_by(
                department_name=form_data['department_name']).one_or_none()

        # check if we have department with such name
        if department:
            date_of_birth = datetime.fromisoformat(form_data['date_of_birth'])
            new_employee = Employee(employee_name=form_data['employee_name'],
                                    date_of_birth=date_of_birth,
                                    salary=form_data['salary'],
                                    department_id=department.department_id)
            department.employee.append(new_employee)
            db.session.commit()
            return {
                        "Message": "Successfully created row in DB",
                        'id': new_employee.employee_id,
                   }, \
                   200
        else:
            return "No such department in DB", 404

    def put(self):
        """
        UPDATE operation with DB for Employee table

        :return: employee list, 200 status code
        """
        form_data = request.form
        # select employee by id
        employee = db.session.query(Employee).filter_by(
                employee_id=form_data['employee_id'],
                ).one_or_none()
        if not employee:
            return "No such employee in DB", 404

        # update employee data
        birth_date = datetime.fromisoformat(form_data['date_of_birth'])
        employee.employee_name = form_data['employee_name']
        employee.date_of_birth = birth_date
        employee.salary = form_data['salary']

        # change employee department
        new_department = db.session.query(Departments).filter_by(
                department_name=form_data['department_name'],
                ).one_or_none()
        if not new_department:
            return "No such department in DB", 404

        employee.parent = new_department
        employee.department_id = new_department.department_id
        db.session.commit()
        return "Successfully updated row in DB", 200

    def delete(self):
        """
        DELETE operation with DB for Employee table

        :return: employee list, 200 status code
        """

        employees_to_del_list = request.json['data']
        employees_to_del = db.session.query(Employee).filter(
                Employee.employee_id.in_(employees_to_del_list))
        num_del = employees_to_del.delete()
        db.session.commit()

        # check if we found rows with such ids
        if not num_del and employees_to_del_list:
            return "Not found such employees", 404
        else:
            return "Successfully deleted data in DB", 200


class DepartmentsCRUD(Resource):
    """
    REST Departments CRUD operations with DB
    """
    def get(self):
        """
        READ operation with DB for Departments table

        :return: employee list, 200 status code
        """
        data = request.args
        # check if we want get only one department
        if 'department_id' in data:
            departments_list = db.session.query(
                    Departments.department_id,
                    Departments.department_name,
                    func.avg(Employee.salary).label('average')).filter_by(
                    department_id=data['department_id']
                    ). \
                join(Employee,
                     Employee.department_id == Departments.department_id,
                     isouter=True). \
                group_by(Departments.department_id).all()
        else:
            departments_list = db.session.query(
                    Departments.department_id,
                    Departments.department_name,
                    func.avg(Employee.salary).label('average')). \
                join(Employee,
                     Employee.department_id == Departments.department_id,
                     isouter=True). \
                group_by(Departments.department_id).all()
        # error handle for wrong department id
        if not departments_list and 'department_id' in data:
            return "No such department in DB", 404

        departments_list = [
                {
                    "0": department[1],
                    "1": float(department[2]) \
                    if department[2] else "No Employees",
                    "DT_RowId": department[0]
                    }
                for department in departments_list
                ]

        return {'data': departments_list}, 200

    def post(self):
        """
        CREATE operation with DB for Departments table

        :return: employee list, 200 status code
        """
        form_data = request.form
        new_department = Departments(
                department_name=form_data['department_name'])
        db.session.add(new_department)
        db.session.commit()
        return {
                       "Message": "Successfully created row in DB",
                       'id': new_department.department_id,
                       }, \
               200

    def put(self):
        """
        UPDATE operation with DB for Departments table

        :return: departments list, 200 status code
        """
        form_data = request.form
        # select department by id
        department = db.session.query(Departments).filter_by(
                department_id=form_data['department_id'],
                ).one_or_none()
        if not department:
            return "No such department in DB", 404

        # update department data
        department.department_name = form_data['department_name']

        db.session.commit()
        return "Successfully updated row in DB", 200

    def delete(self):
        """
        DELETE operation with DB for Departments table

        :return: departments list, 200 status code
        """

        departments_to_del_list = request.json['data']
        departments_to_del = db.session.query(Departments).filter(
                Departments.department_id.in_(departments_to_del_list)).all()
        for department in departments_to_del:
            db.session.delete(department)
        db.session.commit()

        # check if we found rows with such ids
        if not departments_to_del and departments_to_del_list:
            return "Not found such departments", 404
        else:
            return "Successfully deleted data in DB", 200


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
            EmployeeFactory.create_batch(
                    size=10,
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
