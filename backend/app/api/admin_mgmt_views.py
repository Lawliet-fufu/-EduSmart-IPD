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
    """Delete Notification"""
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
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')
    
    # teacher can only see their own classes, admin can see all classes
    if current_user_role == 'teacher':
        classes = Class.query.filter_by(teacher_id=current_user_id).order_by(Class.name).all()
    else:
        classes = Class.query.order_by(Class.name).all()
    
    result = []
    for class_obj in classes:
        teacher = None
        if class_obj.teacher_id:
            teacher_obj = User.query.get(class_obj.teacher_id)
            if teacher_obj:
                teacher = {
                    'id': teacher_obj.id,
                    'full_name': teacher_obj.full_name,
                    'username': teacher_obj.username
                }
        
        result.append({
            'id': class_obj.id,
            'name': class_obj.name,
            'grade': class_obj.grade,
            'teacher': teacher,
            'students_count': class_obj.students_count or 0,
            'avg_attendance': float(class_obj.avg_attendance) if class_obj.avg_attendance else 0,
            'created_at': class_obj.created_at.isoformat() if class_obj.created_at else None
        })
    
    return jsonify(result), 200

@admin_mgmt.route('/classes', methods=['POST'])
@jwt_required
@role_required('admin', 'teacher')
def create_class(*args, **kwargs):
    """Create a class (both admin and teacher can do it).
    Rules:
    - admin: Can create classes for any teacher (teacher_id is optional).
    - teacher: Can only create classes for themselves (ignoring the provided teacher_id and forcing the use of the current user).
    """
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')

    data = request.get_json() or {}
    
    name = data.get('name')
    grade = data.get('grade')
    teacher_id = data.get('teacher_id')
    
    if not name or not grade:
        return jsonify({'message': 'Name and grade are required'}), 400

    # teacher can only create classes for themselves
    if current_user_role == 'teacher':
        teacher_id = current_user_id
    else:
        # admin validate teacher_id
        if teacher_id:
            teacher = User.query.get(teacher_id)
            if not teacher or teacher.role != 'teacher':
                return jsonify({'message': 'Invalid teacher_id'}), 400

    class_obj = Class(
        name=name,
        grade=grade,
        teacher_id=teacher_id,
        # Prevent unauthorized writing to the statistical fields
        students_count=0,
        avg_attendance=0
    )
    
    try:
        db.session.add(class_obj)
        db.session.commit()
        
        return jsonify({
            'id': class_obj.id,
            'name': class_obj.name,
            'grade': class_obj.grade,
            'teacher_id': class_obj.teacher_id,
            'students_count': class_obj.students_count,
            'avg_attendance': float(class_obj.avg_attendance) if class_obj.avg_attendance else 0,
            'message': 'Class created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to create class: {str(e)}'}), 500


@admin_mgmt.route('/classes/<int:class_id>', methods=['PUT'])
@jwt_required
@role_required('admin', 'teacher')
def update_class(class_id, *args, **kwargs):
    """Update a class (admin can update any class; teacher can only update their own classes and only name/grade)."""
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')

    class_obj = Class.query.get_or_404(class_id)

    # teacher can only manage their own classes
    if current_user_role == 'teacher' and class_obj.teacher_id != current_user_id:
        return jsonify({'message': 'You can only manage your own classes'}), 403

    data = request.get_json() or {}

    # fields that can be modified
    if 'name' in data:
        class_obj.name = data['name']
    if 'grade' in data:
        class_obj.grade = data['grade']

    # only admin can modify teacher_id and statistical fields
    if current_user_role == 'admin':
        if 'teacher_id' in data:
            teacher_id = data['teacher_id']
            if teacher_id:
                teacher = User.query.get(teacher_id)
                if not teacher or teacher.role != 'teacher':
                    return jsonify({'message': 'Invalid teacher_id'}), 400
            class_obj.teacher_id = teacher_id
        if 'students_count' in data:
            class_obj.students_count = data['students_count']
        if 'avg_attendance' in data:
            class_obj.avg_attendance = data['avg_attendance']
    
    try:
        db.session.commit()
        
        return jsonify({
            'id': class_obj.id,
            'name': class_obj.name,
            'grade': class_obj.grade,
            'teacher_id': class_obj.teacher_id,
            'students_count': class_obj.students_count,
            'avg_attendance': float(class_obj.avg_attendance) if class_obj.avg_attendance else 0,
            'message': 'Class updated successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update class: {str(e)}'}), 500


@admin_mgmt.route('/classes/<int:class_id>', methods=['DELETE'])
@jwt_required
@role_required('admin', 'teacher')
def delete_class(class_id, *args, **kwargs):
    """Delete the class (Admin can delete any class; Teacher can only delete their own class)."""
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')

    class_obj = Class.query.get_or_404(class_id)

    # teacher can only delete their own classes
    if current_user_role == 'teacher' and class_obj.teacher_id != current_user_id:
        return jsonify({'message': 'You can only manage your own classes'}), 403
    
    try:
        # 1) Delete assignment submissions related to the class
        assignments = Assignment.query.filter_by(class_id=class_id).all()
        for a in assignments:
            AssignmentSubmission.query.filter_by(assignment_id=a.id).delete()
        
        # 2) Delete assignments related to the class
        Assignment.query.filter_by(class_id=class_id).delete()
        
        # 3) 删除该班级下的学生档案（解除关系）
        StudentProfile.query.filter_by(class_id=class_id).delete()
        
        # 4) Delete the class itself
        db.session.delete(class_obj)
        db.session.commit()
        return jsonify({'message': 'Class deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to delete class: {str(e)}'}), 500


@admin_mgmt.route('/classes/<int:class_id>/students', methods=['GET'])
@jwt_required
@role_required('admin', 'teacher')
def get_class_students(class_id, *args, **kwargs):
    """Get the list of students in a class (including grades for three subjects)"""
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')
    
    class_obj = Class.query.get_or_404(class_id)
    
    # Permission check: teacher can only view their own classes
    if current_user_role == 'teacher' and class_obj.teacher_id != current_user_id:
        return jsonify({'message': 'You can only view your own classes'}), 403
    
    # Get all student profiles in the class, ordered by student number
    profiles = StudentProfile.query.filter_by(class_id=class_id).order_by(StudentProfile.student_no).all()
    
    result = []
    for profile in profiles:
        user = User.query.get(profile.user_id)
        if user:
            # Get the student's grades for three subjects (only for the current term)
            grades = Grade.query.filter_by(student_id=profile.user_id, term='current').all()
            grades_dict = {}
            for grade in grades:
                if grade.score is not None:
                    grades_dict[grade.subject] = float(grade.score)
            
            # Calculate average score (only for subjects with grades)
            avg_score = None
            scores = []
            for subject in ['chinese', 'math', 'english']:
                if subject in grades_dict:
                    scores.append(grades_dict[subject])
            if scores:
                avg_score = sum(scores) / len(scores)
            
            computed_avg = round(avg_score, 2) if avg_score is not None else None
            result.append({
                'id': profile.id,
                'user_id': profile.user_id,
                'student_no': profile.student_no,
                'full_name': user.full_name,
                'username': user.username,
                'email': user.email,
                'status': profile.status,
                'attendance_rate': float(profile.attendance_rate) if profile.attendance_rate else 0,
                'avg_grade': float(profile.avg_grade) if profile.avg_grade not in (None, '') else computed_avg,
                'grades': {
                    'chinese': grades_dict.get('chinese'),
                    'math': grades_dict.get('math'),
                    'english': grades_dict.get('english'),
                    'average': computed_avg
                }
            })
    
    return jsonify(result), 200


@admin_mgmt.route('/classes/<int:class_id>/students', methods=['POST'])
@jwt_required
@role_required('admin', 'teacher')
def add_student_to_class(class_id, *args, **kwargs):
    """Add a student to a class (both admin and teacher can do it)."""
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')
    
    class_obj = Class.query.get_or_404(class_id)
    
    # Permission check: teacher can only manage their own classes
    if current_user_role == 'teacher' and class_obj.teacher_id != current_user_id:
        return jsonify({'message': 'You can only manage your own classes'}), 403
    data = request.get_json() or {}
    
    user_id = data.get('user_id')
    term = data.get('term', 'current')
    created_user = None

    if user_id:
        # Validate that the user exists and is a student
        user = User.query.get(user_id)
        if not user or user.role != 'student':
            return jsonify({'message': 'Invalid user_id or user is not a student'}), 400
    else:
        full_name = data.get('full_name')
        student_no_raw = data.get('student_no')
        if not full_name or not student_no_raw:
            return jsonify({'message': 'full_name and student_no are required'}), 400

        username = (data.get('username') or student_no_raw).lower()
        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'Username already exists'}), 400

        password_value = data.get('password_hash') or data.get('password') or 'hashed:123456'
        if not str(password_value).startswith('hashed:'):
            password_value = f'hashed:{password_value}'

        user = User(
            username=username,
            password_hash=password_value,
            full_name=full_name,
            role='student',
            email=data.get('email'),
            avatar=data.get('avatar') or '👤'
        )
        db.session.add(user)
        db.session.flush()
        user_id = user.id
        created_user = user

    # Check if a profile already exists
    existing_profile = StudentProfile.query.filter_by(user_id=user_id).first()
    if existing_profile:
        existing_profile.class_id = class_id
    else:
        existing_profile = StudentProfile(
            user_id=user_id,
            class_id=class_id,
            status='active'
        )
        db.session.add(existing_profile)

    student_no_value = (data.get('student_no') or existing_profile.student_no or '').upper()
    existing_profile.student_no = student_no_value

    if 'status' in data:
        existing_profile.status = data['status']
    if 'attendance_rate' in data:
        existing_profile.attendance_rate = data['attendance_rate']

    # Grade information
    grades_payload = data.get('grades', {})
    subjects = ['chinese', 'math', 'english']
    for subject in subjects:
        if subject in grades_payload:
            score = grades_payload[subject]
            existing_grade = Grade.query.filter_by(
                student_id=user_id,
                subject=subject,
                term=term
            ).first()
            if score is not None and score != '':
                score_value = float(score)
                if score_value < 0 or score_value > 100:
                    return jsonify({'message': f'{subject} score must be between 0 and 100'}), 400
                if existing_grade:
                    existing_grade.score = score_value
                else:
                    new_grade = Grade(
                        student_id=user_id,
                        subject=subject,
                        term=term,
                        score=score_value
                    )
                    db.session.add(new_grade)
            elif existing_grade:
                db.session.delete(existing_grade)

    avg_score = _sync_student_average(user_id, term)

    # Update the number of students in the class
    class_obj.students_count = StudentProfile.query.filter_by(class_id=class_id).count()
    
    try:
        db.session.commit()
        
        return jsonify({
            'id': existing_profile.id,
            'user_id': existing_profile.user_id,
            'class_id': existing_profile.class_id,
            'student_no': existing_profile.student_no,
            'avg_grade': avg_score,
            'message': 'Student added to class successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to add student: {str(e)}'}), 500


@admin_mgmt.route('/classes/<int:class_id>/students/<int:student_id>', methods=['PUT'])
@jwt_required
@role_required('admin', 'teacher')
def update_student_in_class(class_id, student_id, *args, **kwargs):
    """Update the student information in the class (both administrators and teachers can do this)"""
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')
    
    class_obj = Class.query.get_or_404(class_id)
    
    # Permission check: teacher can only manage their own classes
    if current_user_role == 'teacher' and class_obj.teacher_id != current_user_id:
        return jsonify({'message': 'You can only manage your own classes'}), 403
    profile = StudentProfile.query.filter_by(id=student_id, class_id=class_id).first_or_404()
    data = request.get_json() or {}
    
    # Update student profile information
    if 'student_no' in data:
        profile.student_no = data['student_no'].upper()
    if 'status' in data:
        profile.status = data['status']
    if 'attendance_rate' in data:
        profile.attendance_rate = data['attendance_rate']
    
    # Update user information
    user = User.query.get(profile.user_id)
    if user:
        if 'full_name' in data:
            user.full_name = data['full_name']
        if 'email' in data:
            user.email = data['email']
    
    try:
        db.session.commit()
        
        return jsonify({
            'id': profile.id,
            'user_id': profile.user_id,
            'student_no': profile.student_no,
            'status': profile.status,
            'attendance_rate': float(profile.attendance_rate) if profile.attendance_rate else 0,
            'avg_grade': profile.avg_grade,
            'message': 'Student updated successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update student: {str(e)}'}), 500


@admin_mgmt.route('/classes/<int:class_id>/students/<int:student_id>', methods=['DELETE'])
@jwt_required
@role_required('admin', 'teacher')
def remove_student_from_class(class_id, student_id, *args, **kwargs):
    """Remove a student from a class (both admin and teacher can do it)."""
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')
    
    class_obj = Class.query.get_or_404(class_id)
    
    # Permission check: teacher can only manage their own classes
    if current_user_role == 'teacher' and class_obj.teacher_id != current_user_id:
        return jsonify({'message': 'You can only manage your own classes'}), 403
    profile = StudentProfile.query.filter_by(id=student_id, class_id=class_id).first_or_404()
    
    try:
        db.session.delete(profile)
        
        # Update the number of students in the class
        class_obj.students_count = StudentProfile.query.filter_by(class_id=class_id).count()
        
        db.session.commit()
        return jsonify({'message': 'Student removed from class successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to remove student: {str(e)}'}), 500

@admin_mgmt.route('/classes/<int:class_id>/students/<int:student_id>/grades', methods=['GET'])
@jwt_required
@role_required('admin', 'teacher')
def get_student_grades(class_id, student_id, *args, **kwargs):
    """Get the grades of a student in three subjects"""
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')
    
    class_obj = Class.query.get_or_404(class_id)
    
    # Permission check: teacher can only view their own classes
    if current_user_role == 'teacher' and class_obj.teacher_id != current_user_id:
        return jsonify({'message': 'You can only view your own classes'}), 403
    
    profile = StudentProfile.query.filter_by(id=student_id, class_id=class_id).first_or_404()
    
    # Get all grades of the student
    grades = Grade.query.filter_by(student_id=profile.user_id).all()
    
    # Organize grades by subject
    result = {
        'student_id': profile.user_id,
        'student_no': profile.student_no,
        'chinese': None,
        'math': None,
        'english': None
    }
    
    for grade in grades:
        score = float(grade.score) if grade.score else 0
        if grade.subject == 'chinese':
            result['chinese'] = {
                'score': score,
                'term': grade.term,
                'created_at': grade.created_at.isoformat() if grade.created_at else None
            }
        elif grade.subject == 'math':
            result['math'] = {
                'score': score,
                'term': grade.term,
                'created_at': grade.created_at.isoformat() if grade.created_at else None
            }
        elif grade.subject == 'english':
            result['english'] = {
                'score': score,
                'term': grade.term,
                'created_at': grade.created_at.isoformat() if grade.created_at else None
            }
    
    return jsonify(result), 200


@admin_mgmt.route('/classes/<int:class_id>/students/<int:student_id>/grades', methods=['POST'])
@jwt_required
@role_required('admin', 'teacher')
def update_student_grades(class_id, student_id, *args, **kwargs):
    """Update the grades of three subjects for the students"""
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')
    
    class_obj = Class.query.get_or_404(class_id)
        
    # Permission check: teacher can only manage their own classes
    if current_user_role == 'teacher' and class_obj.teacher_id != current_user_id:
        return jsonify({'message': 'You can only manage your own classes'}), 403
    
    profile = StudentProfile.query.filter_by(id=student_id, class_id=class_id).first_or_404()
    data = request.get_json() or {}
    
    term = data.get('term', 'current')
    
    # Update or create grades for three subjects
    subjects = ['chinese', 'math', 'english']
    for subject in subjects:
        if subject in data:
            score = data[subject]
            # Allow updating to None (delete grade)
            # 查找是否已有该科目的成绩
            existing_grade = Grade.query.filter_by(
                student_id=profile.user_id,
                subject=subject,
                term=term
            ).first()
            
            if score is not None and score != '':
                score_value = float(score)
                if score_value < 0 or score_value > 100:
                    return jsonify({'message': f'{subject} score must be between 0 and 100'}), 400
                # If there is a score value, update or create
                if existing_grade:
                    existing_grade.score = score_value
                else:
                    new_grade = Grade(
                        student_id=profile.user_id,
                        subject=subject,
                        term=term,
                        score=score_value
                    )
                    db.session.add(new_grade)
            elif existing_grade:
                # If the score is empty and the grade exists, delete the grade record
                db.session.delete(existing_grade)
    
    try:
        avg_score = _sync_student_average(profile.user_id, term)
        db.session.commit()
        return jsonify({'message': 'Grades updated successfully', 'avg_grade': avg_score}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update grades: {str(e)}'}), 500

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
