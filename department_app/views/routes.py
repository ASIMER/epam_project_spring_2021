from flask import Blueprint, render_template

routes = Blueprint('routes', __name__, static_folder='static')


@routes.route('/')
def main():
    """
    Route for welcome page, it's like menu for further interactions
    """
    return render_template("main.html")


@routes.route('/employees')
def employees():
    """
    Route for employee table, shows all employees in table
    """
    # gather data from db about all employees
    return render_template("employees.html")


@routes.route('/departments')
def departments():
    """
    Route for departments table, shows all departments in table
    """
    # gather data from db about all departments
    return render_template("departments.html")


@routes.route('/employee/<employee_id>')
def employee(employee_id):
    """
    Route for employee table, shows all employees in table
    """
    # gather data from db about all employees
    return render_template("employee.html",
                           employee_id=employee_id)


@routes.route('/department/<department_id>')
def department(department_id):
    """
    Route for employee table, shows all employees in table
    """
    # gather data from db about all employees
    return render_template("department.html",
                           department_id=department_id)
