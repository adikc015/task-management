from flask_smorest import Blueprint, abort
from models.task import Task
from database.engine import SessionLocal
from schemas.task_schema import TaskSchema, TaskCreateSchema, TaskUpdateSchema
from schemas.task_assign_schema import TaskAssignSchema
from models.user import User
from flask_jwt_extended import jwt_required
from authentication.permissions import role_required

blp = Blueprint(
    "tasks",
    "tasks",
    url_prefix="/api/v1/tasks",
    description="Task related operations"
)

@blp.route("/", methods=["GET"])
@jwt_required()
@blp.response(200, TaskSchema(many=True))
def get_tasks():
    session = SessionLocal()
    try:
        return session.query(Task).all()
    finally:
        session.close()

@blp.route("/", methods=['POST'])
@role_required("manager","admin")
@blp.arguments(TaskCreateSchema)
@blp.response(201, TaskSchema)
def create_task(task_data):
    session = SessionLocal()
    try:
        task = Task(**task_data)
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
    finally:
        session.close()
        
@blp.route("/<int:task_id>", methods=['PUT'])
@blp.arguments(TaskUpdateSchema)
@blp.response(201, TaskSchema)
def update_task(update_date, task_id):
    session=SessionLocal()
    try:
        task=session.query(Task).get(task_id)
        if not task:
            abort(404, message="Task not found")
        
        for field, value in update_date.items():
            setattr(task, field, value)
            
        session.commit()
        session.refresh(task)
        return task
    finally:
        session.close()

@blp.route("/<int:task_id>", methods=['DELETE'])      
@blp.response(204)
def delete_task(task_id):
    session=SessionLocal()
    try:
        task=session.query(Task).get(task_id)
        if not task:
            abort(404, message="No task found")

        session.delete(task)
        session.commit()
        return {"message":"Task deleted"}
    finally:
        session.close()
        
@blp.route("/<int:task_id>/assign", methods=['POST'])
@blp.arguments(TaskAssignSchema)
@blp.response(200, TaskSchema)
def assign_users_to_task(data, task_id):
    session=SessionLocal()
    try:
        task=session.query(Task).get(task_id)
        if not task:
            abort(404, message="Task not found")
            
        users=session.query(User).filter(
            User.id.in_(data['user_ids'])
        ).all()
        
        if  not users:
            abort(404, message="No valid users found")
            
        for user in users:
            if user not in task.assigned_users:
                task.assigned_users.append(user)
                
        session.commit()
        session.refresh(task)
        return task
    finally:
        session.close()