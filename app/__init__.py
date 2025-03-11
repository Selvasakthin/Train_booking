import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config

# Global instances
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions (avoid reassigning migrate)
    db.init_app(app)
    migrate.init_app(app, db)  # ✅ Fixed: Avoid redeclaring migrate

    # Import models before migrations
    with app.app_context():
           from .models import Passenger, User, Booking, Train, TrainSeats, BookingPassenger, UserAccounts

    # Import Blueprints
    from .routes import main  # ✅ Ensure 'main' is correctly defined in routes.py
    app.register_blueprint(main)

    return app
