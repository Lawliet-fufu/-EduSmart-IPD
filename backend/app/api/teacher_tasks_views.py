from flask import request, jsonify
from datetime import datetime
from . import teacher_tasks
from app import db
from app.models import Assignment, Class, User
from app.utils.decorators import jwt_required, role_required, get_current_user


@teacher_tasks.route('/assignments', methods=['GET'])
@jwt_required
@role_required('teacher', 'admin', 'student')
def get_assignments(*args, **kwargs):
    """Obtain the list of assignments"""
    pass


@teacher_tasks.route('/assignments', methods=['POST'])
@jwt_required
@role_required('teacher', 'admin', 'student')
def create_assignment(*args, **kwargs):
    """Create an assignment (teacher, admin, and student can all)"""
    pass

@teacher_tasks.route('/assignments/<int:assignment_id>', methods=['PUT'])
@jwt_required
@role_required('teacher', 'admin', 'student')
def update_assignment(assignment_id, *args, **kwargs):
    """Update an assignment (teacher, admin, and student can all)"""
    pass


@teacher_tasks.route('/assignments/<int:assignment_id>', methods=['DELETE'])
@jwt_required
@role_required('teacher', 'admin', 'student')
def delete_assignment(assignment_id, *args, **kwargs):
    """Delete an assignment (teacher, admin, and student can all)"""
    pass


@teacher_tasks.route('/ai/command', methods=['POST'])
def ai_command():
    # The "Agent Mode": 
    # Receives a natural language string, processes it via ai_service, 
    # and maps it to a system function (e.g., triggering a database insert for homework)
    return "AI Command Processed"
