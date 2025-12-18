from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import config

db = SQLAlchemy()
jwt = JWTManager()

def create_app(config_name='default'):
    app = Flask(__name__)
    app_config = config[config_name]()
    app.config.from_object(app_config)
    app_config.init_app(app)

    db.init_app(app)
    # CORS configuration - allow frontend origin
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://127.0.0.1:5173", "http://localhost:5173"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })

    # JWT configuration
    app.config.setdefault('JWT_SECRET_KEY', app.config.get('SECRET_KEY', 'change-this-jwt-secret'))
    app.config.setdefault('JWT_ACCESS_TOKEN_EXPIRES', False)  # Token 不过期（开发环境）
    app.config.setdefault('JWT_TOKEN_LOCATION', ['headers'])  # 从请求头读取 token
    app.config.setdefault('JWT_HEADER_NAME', 'Authorization')  # Authorization 头
    app.config.setdefault('JWT_HEADER_TYPE', 'Bearer')  # Bearer token
    jwt.init_app(app)

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
