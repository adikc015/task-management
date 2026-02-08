from flask_smorest import Blueprint, abort 

from schemas.department_schema import DepartmentCreateSchema, DepartmentSchema
from models.department import Department
from database.session import SessionLocal
from authentication.permissions import role_required

blp=Blueprint(
    "departments",
    "departments",
    url_prefix="/api/v1/departments",
    description="Department management (Admin only)"
    )

@blp.route("/", methods=['POST'])
@role_required("admin")
@blp.arguments(DepartmentCreateSchema)
@blp.response(201, DepartmentSchema)
def create_department(data):
    session=SessionLocal()
    try:
        if session.query(Department).filter_by(name=data["name"]).first():
            abort(400, message="Department already exists.")
            
        department=Department(name=data["name"])
        session.add(department)
        session.commit()
        session.refresh(department)
        return department
    finally:
        session.close()
        
@blp.route("/", methods=['GET'])
@role_required("admin")
@blp.response(200, DepartmentSchema(many=True))
def list_departments():
    session=SessionLocal()
    try:
        return session.query(Department).all()
    finally:
        session.close()