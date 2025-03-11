import os
from app import create_app, db

# Create the Flask app instance
app = create_app()

if __name__ == '__main__':
    with app.app_context():  
        db.create_all()  # Ensure tables exist only if Flask-Migrate is NOT used
        
    port = int(os.environ.get("PORT", 5000))  # Set default port to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
