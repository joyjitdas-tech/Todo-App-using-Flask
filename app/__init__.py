from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login_page"

    # Blueprints
    from .routes.auth import auth_bp
    from .routes.tasks import task_bp

    # Blueprints
    from app.routes import auth_bp, task_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app