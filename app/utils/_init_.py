# app/__init__.py
from flask import Flask
from app.routes import register_routes  # Import a function to register routes

def create_app():
    app = Flask(__name__)
    app.secret_key = 'abc123'
    
    # Register routes
    register_routes(app)
    
    return app
