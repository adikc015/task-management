from flask import Flask, render_template
from flask_smorest import Api, Blueprint
from flask_jwt_extended import JWTManager
from config import settings

from routes.tasks import blp as tasks_blp
from routes.auth import blp as auth_blp
from routes.users import blp as users_blp
from routes.department import blp as dept_blp
from routes.projects import blp as project_blp

def create_app():
    app=Flask(__name__)

    @app.get("/")
    def home():
        return render_template("index.html")

    app.config["API_TITLE"] = settings.API_TITLE
    app.config["API_VERSION"] = settings.API_VERSION
    app.config["OPENAPI_VERSION"] = settings.OPENAPI_VERSION

    app.config["OPENAPI_URL_PREFIX"] = settings.OPENAPI_URL_PREFIX
    app.config["OPENAPI_SWAGGER_UI_PATH"] = settings.OPENAPI_SWAGGER_UI_PATH
    app.config["OPENAPI_SWAGGER_UI_URL"] = settings.OPENAPI_SWAGGER_UI_URL

    app.config["SQLALCHEMY_DATABASE_URI"] = settings.APP_SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    
    app.config["SECRET_KEY"] = settings.SECRET_KEY
    app.config["JWT_SECRET_KEY"] = settings.JWT_SECRET_KEY
    
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
    app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.FLASK_DEBUG)