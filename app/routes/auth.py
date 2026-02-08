from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash

from database.engine import SessionLocal
from models.user import User
from marshmallow import Schema, fields

blp = Blueprint(
    "auth",
    "auth",
    url_prefix="/api/v1/auth",
    description="Authenticcation operations"
)

class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    
@blp.route("/login", methods=['POST'])
@blp.arguments(LoginSchema)
def login(data):
    session=SessionLocal()
    try:
        user=session.query(User).filter_by(email=data['email']).first()
        
        if not user or not check_password_hash(user.password_hash, data['password']):
            abort(401, message="Invalid credentials")
            
        token = create_access_token(identity=str(user.id))
        
        return {
            "access_token":token
        }
        
    finally:
        session.close()