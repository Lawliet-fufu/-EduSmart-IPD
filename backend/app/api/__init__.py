from flask import Blueprint

auth = Blueprint('auth', __name__)
teacher_tasks = Blueprint('teacher_tasks', __name__)
student_learning = Blueprint('student_learning', __name__)
admin_mgmt = Blueprint('admin_mgmt', __name__)

from . import auth_views, teacher_tasks_views, student_learning_views, admin_mgmt_views
