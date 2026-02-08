# from database.engine import SessionLocal
# from models.department import Department
# from models.user import User
# from models.task import  Task
# from models.project import Project

# def run():
#     session=SessionLocal()
    
#     try:
#         dept = Department(name="employee")
#         session.add(dept)
#         session.commit()
#         session.refresh(dept)
        
#         user = User(
#             name="Dev",
#             email='dev@gmail.com',
#             password_hash="hashes_pwd",
#             role="Employee",
#             department_id=dept.id
#         )
        
#         session.add(user)
#         session.commit()
#         session.refresh(user)
        
#         project = Project(
#             name="Task Management System",
#             department_id = dept.id
#         )
        
#         session.add(project)
#         session.commit()
#         session.refresh(project)
        
#         task = Task(
#             title="Implement schema models",
#             description="Create schema",
#             priority="High",
#             project_id = project.id
#         )
#         session.add(task)
#         session.commit()
#         session.refresh(task)
        
#         print("Data inserted successfully!")
        
#     except Exception as e:
#         session.rollback()
#         print("Error: ", e)
    
#     finally:
#         session.close()
        
# if __name__=="__main__":
#     run()


from models.department import Department
from werkzeug.security import generate_password_hash
from database.engine import SessionLocal
from models.user import User

session = SessionLocal()

users = session.query(User).all()
for user in users:
    user.password_hash = generate_password_hash("password123")

session.commit()
session.close()
