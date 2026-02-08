from functools import wraps
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_smorest import abort

from database.engine import SessionLocal
from models.user import User

def role_required(*allowed_roles):
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            session=SessionLocal()
            try:
                user_id = int(get_jwt_identity())
                user = session.query(User).get(user_id)
                
                if not user:
                    abort(401, message="User not found")
                    
                if user.role not in allowed_roles:
                    abort(403, message="Access forbidden")
                
                return func(*args, **kwargs)
            finally:
                session.close()
        return wrapper
    return decorator