from uuid import uuid4

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Departments(db.Model):
    """
    this class represents department in db

    department_id: Integer - department id in db\n
    department_name: String(50) - department name\n
    employee_id: LargeBinary(16) - relationship Employee to Departments
    """
    __tablename__ = 'Departments'
    department_id = db.Column(db.String(36),
                              primary_key=True,
                              index=True,
                              default=uuid4)

    department_name = db.Column(db.String(50), nullable=False, index=True)
    employee = db.relationship('Employee',
                              backref=db.backref('Departments', lazy=False),
                              cascade="all, delete")

    def __repr__(self):
        return '<Department %r with name %r>' % \
               (self.department_id, self.department_name)


class Employee(db.Model):
    """
    this class represents employee in db

    employee_id: LargeBinary(16) - employee id in db\n
    employee_name: String(50) - employee full name\n
    date_of_birth: Date - employee birthdate\n
    salary: Integer - salary of employee\n
    department_id: LargeBinary(16) - relationship Employee to Departments
    """
    __tablename__ = 'Employee'
    employee_id = db.Column(db.String(36),
                            primary_key=True,
                            index=True,
                            default=uuid4)

    employee_name = db.Column(db.String(50), index=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Integer, nullable=False)
    # foreign relation
    department_id = db.Column(db.String(36),
                              db.ForeignKey('Departments.department_id'),
                              nullable=False)

    def __repr__(self):
        return '<Employee %r with name %r, birthdate %r and salary %r>' % \
               (self.employee_id, self.employee_name,
                self.date_of_birth, self.salary)
