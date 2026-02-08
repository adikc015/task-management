from flask_smorest import Blueprint, abort
from werkzeug.security import generate_password_hash

from database.engine import SessionLocal
from models.user import User
from schemas.user_schema import UserSchema, UserCreateSchema
from authentication.permissions import role_required

blp = Blueprint(
    "users",
    "users",
    url_prefix="/api/v1/users",
    description="User maangement (Admin only)"
)

@blp.route("/", methods=['POST'])
@role_required("admin")
@blp.arguments(UserCreateSchema)
@blp.response(201, UserSchema)
def create_user(data):
    session=SessionLocal()
    try:
        if session.query(User).filter_by(email=data["email"]).first():
            abort(400, message="Email already exists")
        
        user = User(
            name=data['name'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            role=data['role'],
            department_id=data['department_id']
        )
        
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    finally:
        session.close()
        
@blp.route("/", methods=['GET'])
@role_required("admin")
@blp.response(200, UserSchema(many=True))
def list_users():
    session=SessionLocal()
    try:
        return session.query(User).all()
    finally:
        session.close()