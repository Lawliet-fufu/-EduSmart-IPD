from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import config

db = SQLAlchemy()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    CORS(app)

    # Register Blueprints
    from .api import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')

    from .api import teacher_tasks as teacher_tasks_blueprint
    app.register_blueprint(teacher_tasks_blueprint, url_prefix='/api/teacher-tasks')

    from .api import student_learning as student_learning_blueprint
    app.register_blueprint(student_learning_blueprint, url_prefix='/api/student-learning')

    from .api import admin_mgmt as admin_mgmt_blueprint
    app.register_blueprint(admin_mgmt_blueprint, url_prefix='/api/admin')

    return app
