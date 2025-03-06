import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

db = SQLAlchemy()
migrate=Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Import Blueprints
    from .routes import main  # Ensure 'main' is defined in routes.py
    app.register_blueprint(main)

    with app.app_context():
        from .models import Passenger, User  # ✅ Fixed import error


    return app
