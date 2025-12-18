from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from app.models import User
import traceback


def jwt_required(f):
    """JWT验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
        except Exception as e:
            # 捕获所有 JWT 相关错误（包括 NoAuthorizationError, JWTDecodeError 等）
            auth_header = request.headers.get('Authorization', 'Not found')
            print(f"JWT Error: {type(e).__name__}: {str(e)}")
            print(f"Authorization header: {auth_header}")
            print(f"Request path: {request.path}")
            print(f"Request method: {request.method}")
            # 打印完整的错误堆栈（仅在开发环境）
            if hasattr(request, 'app') and request.app.config.get('DEBUG'):
                print(traceback.format_exc())
            return jsonify({'message': 'Token is missing or invalid'}), 401
        return f(*args, **kwargs)
    return decorated_function


def role_required(*allowed_roles):
    """角色权限验证装饰器"""
    def decorator(f):
        @wraps(f)
        @jwt_required
        def decorated_function(*args, **kwargs):
            try:
                claims = get_jwt()
                user_role = claims.get('role')
                
                if user_role not in allowed_roles:
                    return jsonify({'message': 'Insufficient permissions'}), 403
                
                # 将当前用户ID和角色注入到kwargs中，方便后续使用
                # JWT identity is stored as string, convert to int for database queries
                user_id_str = get_jwt_identity()
                kwargs['current_user_id'] = int(user_id_str) if user_id_str else None
                kwargs['current_user_role'] = user_role
                
            except Exception as e:
                return jsonify({'message': 'Permission verification failed'}), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def get_current_user():
    """获取当前登录用户对象"""
    try:
        user_id_str = get_jwt_identity()
        if user_id_str:
            user_id = int(user_id_str)
            return User.query.get(user_id)
        return None
    except:
        return None

