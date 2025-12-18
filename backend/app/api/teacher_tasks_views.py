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
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')
    
    # All roles can view all assignments (students and teachers have the same permissions)
    query = Assignment.query
    
    # Support filtering by status
    status = request.args.get('status')
    if status:
        query = query.filter_by(status=status)
    
    # Support filtering by subject
    subject = request.args.get('subject')
    if subject:
        query = query.filter_by(subject=subject)
    
    assignments = query.order_by(Assignment.due_date.desc()).all()
    
    # Count the completion status of each assignment
    from app.models import AssignmentSubmission
    result = []
    for assignment in assignments:
        total_students = 0
        completed_count = 0
        
        if assignment.class_id:
            class_obj = Class.query.get(assignment.class_id)
            if class_obj:
                total_students = class_obj.students_count or 0
                completed_count = AssignmentSubmission.query.filter_by(
                    assignment_id=assignment.id,
                    status='submitted'
                ).count()
        
        result.append({
            'id': assignment.id,
            'title': assignment.title,
            'subject': assignment.subject,
            'description': assignment.description,
            'dueDate': assignment.due_date.strftime('%Y-%m-%d') if assignment.due_date else None,
            'status': assignment.status,
            'class_id': assignment.class_id,
            'teacher_id': assignment.teacher_id,
            'students': total_students,
            'completed': completed_count,
            'created_at': assignment.created_at.isoformat() if assignment.created_at else None
        })
    
    return jsonify(result), 200


@teacher_tasks.route('/assignments', methods=['POST'])
@jwt_required
@role_required('teacher', 'admin', 'student')
def create_assignment(*args, **kwargs):
    """Create an assignment (teacher, admin, and student can all)"""
    current_user_id = kwargs.get('current_user_id')
    data = request.get_json() or {}
    
    # Verify Required Fields
    title = data.get('title')
    subject = data.get('subject')
    due_date_str = data.get('dueDate')
    class_id = data.get('class_id')
    
    if not title or not subject:
        return jsonify({'message': 'Title and subject are required'}), 400
    
    # Verify whether the subject is a valid value
    if subject not in ['chinese', 'math', 'english']:
        return jsonify({'message': 'Subject must be one of: chinese, math, english'}), 400
    
    # Parsing date
    due_date = None
    if due_date_str:
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        except:
            return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
    
    # Create Assignment
    assignment = Assignment(
        title=title,
        subject=subject,
        description=data.get('description', ''),
        due_date=due_date,
        status=data.get('status', 'pending'),
        class_id=class_id,
        teacher_id=current_user_id
    )
    
    try:
        db.session.add(assignment)
        db.session.commit()
        
        return jsonify({
            'id': assignment.id,
            'title': assignment.title,
            'subject': assignment.subject,
            'description': assignment.description,
            'dueDate': assignment.due_date.strftime('%Y-%m-%d') if assignment.due_date else None,
            'status': assignment.status,
            'class_id': assignment.class_id,
            'teacher_id': assignment.teacher_id,
            'message': 'Assignment created successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to create assignment: {str(e)}'}), 500

@teacher_tasks.route('/assignments/<int:assignment_id>', methods=['PUT'])
@jwt_required
@role_required('teacher', 'admin', 'student')
def update_assignment(assignment_id, *args, **kwargs):
    """Update an assignment (teacher, admin, and student can all)"""
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')
    
    assignment = Assignment.query.get_or_404(assignment_id)
    
    # Permission check: Teachers can only modify the assignments they have set, while students can modify any assignment.
    if current_user_role == 'teacher' and assignment.teacher_id != current_user_id:
        return jsonify({'message': 'You can only update your own assignments'}), 403
    
    data = request.get_json() or {}
    
    # Update field
    if 'title' in data:
        assignment.title = data['title']
    if 'subject' in data:
        if data['subject'] not in ['chinese', 'math', 'english']:
            return jsonify({'message': 'Subject must be one of: chinese, math, english'}), 400
        assignment.subject = data['subject']
    if 'description' in data:
        assignment.description = data['description']
    if 'dueDate' in data:
        if data['dueDate']:
            try:
                assignment.due_date = datetime.strptime(data['dueDate'], '%Y-%m-%d').date()
            except:
                return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400
        else:
            assignment.due_date = None
    if 'status' in data:
        assignment.status = data['status']
    if 'class_id' in data:
        assignment.class_id = data['class_id']
    
    try:
        db.session.commit()
        
        return jsonify({
            'id': assignment.id,
            'title': assignment.title,
            'subject': assignment.subject,
            'description': assignment.description,
            'dueDate': assignment.due_date.strftime('%Y-%m-%d') if assignment.due_date else None,
            'status': assignment.status,
            'message': 'Assignment updated successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to update assignment: {str(e)}'}), 500


@teacher_tasks.route('/assignments/<int:assignment_id>', methods=['DELETE'])
@jwt_required
@role_required('teacher', 'admin', 'student')
def delete_assignment(assignment_id, *args, **kwargs):
    """Delete an assignment (teacher, admin, and student can all)"""
    current_user_id = kwargs.get('current_user_id')
    current_user_role = kwargs.get('current_user_role')
    
    assignment = Assignment.query.get_or_404(assignment_id)
    
    # Permission check: Teachers can only delete the assignments they have set, while students can delete any assignment.
    if current_user_role == 'teacher' and assignment.teacher_id != current_user_id:
        return jsonify({'message': 'You can only delete your own assignments'}), 403
    
    try:
        db.session.delete(assignment)
        db.session.commit()
        return jsonify({'message': 'Assignment deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Failed to delete assignment: {str(e)}'}), 500


@teacher_tasks.route('/ai/command', methods=['POST'])
def ai_command():
    # The "Agent Mode": 
    # Receives a natural language string, processes it via ai_service, 
    # and maps it to a system function (e.g., triggering a database insert for homework)
    return "AI Command Processed"
