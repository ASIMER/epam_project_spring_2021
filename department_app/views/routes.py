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
    employee_list = []
    return render_template("employees.html",
                           employee_list=employee_list)


@routes.route('/departments')
def departments():
    """
    Route for departments table, shows all departments in table
    """
    # gather data from db about all departments
    departments_list = []
    return render_template("departments.html",
                           employee_list=departments_list)
