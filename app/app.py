from flask import Flask
from flask_smorest import Api, Blueprint
from flask_jwt_extended import JWTManager

from routes.tasks import blp as tasks_blp
from routes.auth import blp as auth_blp
from routes.users import blp as users_blp
from routes.department import blp as dept_blp
from routes.projects import blp as project_blp

def create_app():
    app=Flask(__name__)

    app.config["API_TITLE"] = "Task Management API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"

    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    app.config["SQLACHEMY_DATABASE_URI"] = "mysql+pymysql://root:Ghy%401234@localhost:3036/task_manager"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
    
    app.config["SECRET_KEY"] = "abcd"
    app.config["JWT_SECRET_KEY"] = "abcd"
    
    # db.init_app(app)
    
    api=Api(app)
    jwt = JWTManager(app)

    blp=Blueprint("health", "health", url_prefix="/api/v1")

    @blp.route('/health')
    def health():
        return {'status':'OK'}
    
    api.register_blueprint(tasks_blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(users_blp)
    api.register_blueprint(dept_blp)
    api.register_blueprint(project_blp)
    return app

app=create_app()

if __name__=="__main__":
    app.run(debug=True)