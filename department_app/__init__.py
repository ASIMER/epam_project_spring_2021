from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from department_app.config import Config
from department_app.models.models import db

app = Flask(__name__)
# load variables from object and registering in app
app.config.from_object(Config())
# app.wsgi_app = Middleware(app.wsgi_app)
api = Api(app)
# registering app in flask_sqlalchemy db object
db.init_app(app)
# registering app and db to enable migration control
migrate = Migrate(app, db)

# register blueprint
from department_app.views.routes import routes
app.register_blueprint(routes,
                       static_folder='static',
                       static_url_path='/static')

# register FlaskRESTFull classes
from department_app.rest.routes import \
    EmployeeCRUD, DepartmentsCRUD, TestDBData
api.add_resource(EmployeeCRUD, "/employee_crud")
api.add_resource(DepartmentsCRUD, "/departments_crud")
api.add_resource(TestDBData, "/test_db_data")
