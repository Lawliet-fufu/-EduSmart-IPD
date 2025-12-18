from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, teacher, student
    email = db.Column(db.String(100))
    avatar = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class Class(db.Model):
    __tablename__ = 'classes'

    id = db.Column('class_id', db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    grade = db.Column(db.String(50), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    students_count = db.Column(db.Integer, default=0)
    avg_attendance = db.Column(db.Numeric(5, 2), default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'

    id = db.Column('profile_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    student_no = db.Column(db.String(50))
    status = db.Column(db.String(20), default='active')
    attendance_rate = db.Column(db.Numeric(5, 2), default=0)
    avg_grade = db.Column(db.Numeric(5, 2))


class Assignment(db.Model):
    __tablename__ = 'assignments'

    id = db.Column('assignment_id', db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    # 仅允许 'chinese'（语文）、'math'（数学）、'english'（英语）
    subject = db.Column(db.Enum('chinese', 'math', 'english', name='subject_type'), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')
    class_id = db.Column(db.Integer, db.ForeignKey('classes.class_id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class AssignmentSubmission(db.Model):
    __tablename__ = 'assignment_submissions'

    id = db.Column('submission_id', db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.assignment_id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    submit_time = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='submitted')
    score = db.Column(db.Numeric(5, 2))
    feedback = db.Column(db.Text)


class Notice(db.Model):
    __tablename__ = 'notices'

    id = db.Column('notice_id', db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    date = db.Column(db.Date, nullable=False)
    priority = db.Column(db.String(20), default='normal')
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column('grade_id', db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    subject = db.Column(db.Enum('chinese', 'math', 'english', name='subject_type'), nullable=False)
    term = db.Column(db.String(50))
    score = db.Column(db.Numeric(5, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class AIFile(db.Model):
    __tablename__ = 'ai_files'

    id = db.Column('ai_file_id', db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50))
    source = db.Column(db.String(20), default='upload')
    status = db.Column(db.String(20), default='uploaded')
    analysis_summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)


class UserPreferences(db.Model):
    __tablename__ = 'user_preferences'

    # 1:1 关系，主键即外键
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
    dark_mode = db.Column(db.Boolean, default=False, nullable=False)
    language = db.Column(db.String(10), default='en', nullable=False)
    notifications = db.Column(db.Boolean, default=True, nullable=False)
    email_alerts = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
