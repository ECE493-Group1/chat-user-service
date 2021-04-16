import os

from sqlalchemy import create_engine

from flask import Flask
from flask_cors import CORS

def create_app(test_config=None, db_string=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
    
    if db_string:
        app.config["DATABASE"] = db_string
    else:
        app.config["DATABASE"] = 'sqlite:///' + os.path.join(app.instance_path, "user_service.db")

    app.config["MAIL_SERVER"] = "smtp.gmail.com"
    app.config["MAIL_PORT"] = 587
    app.config["MAIL_USE_TLS"] = True
    app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_USERNAME")

    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .database import init_db
    init_db(app.config["DATABASE"])

    from .database import session
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        session.remove()

    from .mail import mail
    mail.init_app(app)

    from app import routes
    app.register_blueprint(routes.bp)

    

    return app


