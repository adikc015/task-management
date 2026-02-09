from flask_smorest import Blueprint, abort

from database.engine import SessionLocal
from models.project import Project
from models.department import Department
from schemas.project_schema import ProjectCreateSchema, ProjectSchema
from authentication.permissions import role_required

blp = Blueprint(
    "projects",
    "projects",
    url_prefix="/api/v1/projects",
    description="Project Management (Admin, Manager)"
)

@blp.route("/", methods=['POST'])
@role_required("admin","manager")
@blp.arguments(ProjectCreateSchema)
@blp.response(201, ProjectSchema)
def create_project(data):
    session=SessionLocal()
    try:
        department=session.query(Department).get(data["department_id"])
        
        if not department:
            abort(400, message="Invalid department_id")

        project=Project(
            name=data["name"],
            department_id=data["department_id"]
        )
        
        session.add(project)
        session.commit()
        session.refresh(project)
        return project
    finally:
        session.close()
        
@blp.route("/", methods=['GET'])
@role_required("admin", "manager")
@blp.response(200, ProjectSchema(many=True))
def list_projects():
    session=SessionLocal()
    try:
        return session.query(Department).all()
    finally:
        session.close()