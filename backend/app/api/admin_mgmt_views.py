from flask import request, jsonify
from datetime import datetime
from . import admin_mgmt
from app import db
from app.models import Notice, User, Class, StudentProfile, Grade, Assignment, AssignmentSubmission
from app.utils.decorators import jwt_required, role_required
def _sync_student_average(student_id, term='current'):
    """Recalculate and persist a student's average score for the specified term."""
    grades = Grade.query.filter_by(student_id=student_id, term=term).all()
    scores = [float(grade.score) for grade in grades if grade.score is not None]
    avg_score = None
    if scores:
        avg_score = round(sum(scores) / len(scores), 2)
    profile = StudentProfile.query.filter_by(user_id=student_id).first()
    if profile:
        profile.avg_grade = avg_score
    return avg_score


@admin_mgmt.route('/notices', methods=['GET'])
@jwt_required
def get_notices(*args, **kwargs):
    """Get the list of notices (all roles can view)"""
    # Support filtering by priority and category
    priority = request.args.get('priority')
    category = request.args.get('category')
    
    query = Notice.query
    if priority:
        query = query.filter_by(priority=priority)
    if category:
        query = query.filter_by(category=category)
    
    notices = query.order_by(Notice.date.desc(), Notice.created_at.desc()).all()
    
    result = []
    for notice in notices:
        author = None
        if notice.author_id:
            author_obj = User.query.get(notice.author_id)
            if author_obj:
                author = {
                    'id': author_obj.id,
                    'full_name': author_obj.full_name,
                    'username': author_obj.username
                }
        
        result.append({
            'id': notice.id,
            'title': notice.title,
            'content': notice.content,
            'author': author,
            'date': notice.date.strftime('%Y-%m-%d') if notice.date else None,
            'priority': notice.priority,
            'category': notice.category,
            'created_at': notice.created_at.isoformat() if notice.created_at else None
        })
    
    return jsonify(result), 200


@admin_mgmt.route('/notices/<int:notice_id>', methods=['GET'])
@jwt_required
def get_notice(notice_id, *args, **kwargs):
    """Get a single notice detail"""
    notice = Notice.query.get_or_404(notice_id)
    
    author = None
    if notice.author_id:
        author_obj = User.query.get(notice.author_id)
        if author_obj:
            author = {
                'id': author_obj.id,
                'full_name': author_obj.full_name,
                'username': author_obj.username
            }
    
    return jsonify({
        'id': notice.id,
        'title': notice.title,
        'content': notice.content,
        'author': author,
        'date': notice.date.strftime('%Y-%m-%d') if notice.date else None,
        'priority': notice.priority,
        'category': notice.category,
        'created_at': notice.created_at.isoformat() if notice.created_at else None
    }), 200


@admin_mgmt.route('/notices', methods=['POST'])
@jwt_required
@role_required('admin', 'teacher')
def create_notice(*args, **kwargs):
    """Create a notice (admin and teacher can both)"""
    current_user_id = kwargs.get('current_user_id')
    data = request.get_json() or {}
    
    title = data.get('title')
    content = data.get('content')
    date_str = data.get('date')
    
    if not title or not content:
        return jsonify({'message': 'Title and content are required'}), 400
    
    # Analysis date
    notice_date = datetime.now().date()
    if date_str:
        try:
            notice_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    notice = Notice(
        title=title,
        content=content,
        author_id=current_user_id,
        date=notice_date,
        priority=data.get('priority', 'normal'),
        category=data.get('category', '')
    )
    
    try:
        db.session.add(notice)
        db.session.commit()
        
        return jsonify({
            'id': notice.id,
            'title': notice.title,
            'content': notice.content,
            'author_id': notice.author_id,
            'date': notice.date.strftime('%Y-%m-%d'),
            'priority': notice.priority,
            'category': notice.category,
            'message': 'Notice created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to create notice: {str(e)}'}), 500


@admin_mgmt.route('/notices/<int:notice_id>', methods=['PUT'])
@jwt_required
@role_required('admin', 'teacher')
def update_notice(notice_id, *args, **kwargs):
    """Update a notice"""
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')
    
    notice = Notice.query.get_or_404(notice_id)
    
    # Permission adjustment: Allow teacher to update any notification (if it is necessary to restrict access to only the individual, the following judgment can be restored)
    # if current_user_role == 'teacher' and notice.author_id != current_user_id:
    #     return jsonify({'message': 'You can only update your own notices'}), 403
    
    data = request.get_json() or {}
    
    if 'title' in data:
        notice.title = data['title']
    if 'content' in data:
        notice.content = data['content']
    if 'date' in data:
        if data['date']:
            try:
                notice.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
            except:
                return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
    if 'priority' in data:
        notice.priority = data['priority']
    if 'category' in data:
        notice.category = data['category']
    
    try:
        db.session.commit()
        
        return jsonify({
            'id': notice.id,
            'title': notice.title,
            'content': notice.content,
            'date': notice.date.strftime('%Y-%m-%d'),
            'priority': notice.priority,
            'category': notice.category,
            'message': 'Notice updated successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update notice: {str(e)}'}), 500


@admin_mgmt.route('/notices/<int:notice_id>', methods=['DELETE'])
@jwt_required
@role_required('admin', 'teacher')
def delete_notice(notice_id, *args, **kwargs):
    """删除通知"""
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')
    
    notice = Notice.query.get_or_404(notice_id)
    
    # Permission adjustment: Allow teacher to delete any notification (if it is necessary to restrict access to only the individual, the following judgment can be restored)
    # if current_user_role == 'teacher' and notice.author_id != current_user_id:
    #     return jsonify({'message': 'You can only delete your own notices'}), 403
    
    try:
        db.session.delete(notice)
        db.session.commit()
        return jsonify({'message': 'Notice deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to delete notice: {str(e)}'}), 500


@admin_mgmt.route('/classes', methods=['GET'])
@jwt_required
@role_required('admin', 'teacher')
def get_classes(*args, **kwargs):
    """Get the list of classes"""
    pass

@admin_mgmt.route('/classes', methods=['POST'])
@jwt_required
@role_required('admin', 'teacher')
def create_class(*args, **kwargs):
    """Create a class (both admin and teacher can do it).
    Rules:
    - admin: Can create classes for any teacher (teacher_id is optional).
    - teacher: Can only create classes for themselves (ignoring the provided teacher_id and forcing the use of the current user).
    """
    pass


@admin_mgmt.route('/classes/<int:class_id>', methods=['PUT'])
@jwt_required
@role_required('admin', 'teacher')
def update_class(class_id, *args, **kwargs):
    """Update a class (admin can update any class; teacher can only update their own classes and only name/grade)."""
    pass


@admin_mgmt.route('/classes/<int:class_id>', methods=['DELETE'])
@jwt_required
@role_required('admin', 'teacher')
def delete_class(class_id, *args, **kwargs):
    """Delete the class (Admin can delete any class; Teacher can only delete their own class)."""
    pass


@admin_mgmt.route('/classes/<int:class_id>/students', methods=['GET'])
@jwt_required
@role_required('admin', 'teacher')
def get_class_students(class_id, *args, **kwargs):
    """Get the list of students in a class (including grades for three subjects)"""
    pass


@admin_mgmt.route('/classes/<int:class_id>/students', methods=['POST'])
@jwt_required
@role_required('admin', 'teacher')
def add_student_to_class(class_id, *args, **kwargs):
    """Add a student to a class (both admin and teacher can do it)."""
    pass


@admin_mgmt.route('/classes/<int:class_id>/students/<int:student_id>', methods=['PUT'])
@jwt_required
@role_required('admin', 'teacher')
def update_student_in_class(class_id, student_id, *args, **kwargs):
    """Update the student information in the class (both administrators and teachers can do this)"""


@admin_mgmt.route('/classes/<int:class_id>/students/<int:student_id>', methods=['DELETE'])
@jwt_required
@role_required('admin', 'teacher')
def remove_student_from_class(class_id, student_id, *args, **kwargs):
    """Remove a student from a class (both admin and teacher can do it)."""
    pass

@admin_mgmt.route('/classes/<int:class_id>/students/<int:student_id>/grades', methods=['GET'])
@jwt_required
@role_required('admin', 'teacher')
def get_student_grades(class_id, student_id, *args, **kwargs):
    """Get the grades of a student in three subjects"""
    pass


@admin_mgmt.route('/classes/<int:class_id>/students/<int:student_id>/grades', methods=['POST'])
@jwt_required
@role_required('admin', 'teacher')
def update_student_grades(class_id, student_id, *args, **kwargs):
    """Update the grades of three subjects for the students"""


@admin_mgmt.route('/users', methods=['GET'])
@jwt_required
@role_required('admin')
def get_users(*args, **kwargs):
    """Get the list of users (admin only)"""
    # Support filtering by role
    role = request.args.get('role')
    
    query = User.query
    if role:
        query = query.filter_by(role=role)
    
    users = query.order_by(User.created_at.desc()).all()
    
    result = []
    for user in users:
        result.append({
            'id': user.id,
            'username': user.username,
            'full_name': user.full_name,
            'role': user.role,
            'email': user.email,
            'avatar': user.avatar,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat() if user.created_at else None
        })
    
    return jsonify(result), 200


@admin_mgmt.route('/classes/<int:class_id>/grade-distribution', methods=['GET'])
@jwt_required
@role_required('admin', 'teacher')
def get_class_grade_distribution(class_id, *args, **kwargs):
    """Return the grade distribution for a class (0-100, one bucket per point). Includes four curves for Chinese, Math, English, and Average."""
    pass


# Dashboard summary (reducing multiple requests at the front end)
@admin_mgmt.route('/dashboard/summary', methods=['GET'])
@jwt_required
@role_required('admin', 'teacher', 'student')
def dashboard_summary(*args, **kwargs):
    pass
