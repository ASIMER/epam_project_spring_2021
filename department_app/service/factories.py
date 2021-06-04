from department_app.models.models import *
import factory
from department_app import db


class DepartmentFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Factory for Departments table
    """

    department_id = factory.Sequence(lambda x: uuid4())
    department_name = factory.Faker('company')

    class Meta:
        sqlalchemy_session = db.session
        model = Departments


class EmployeeFactory(factory.alchemy.SQLAlchemyModelFactory):
    """
    Factory for Employee table
    """
    employee_id = factory.Sequence(lambda x: uuid4())
    employee_name = factory.Faker('name')
    date_of_birth = factory.Faker('date')
    salary = factory.Faker('random_number')
    department_id = factory.Faker('company')

    class Meta:
        sqlalchemy_session = db.session
        model = Employee
