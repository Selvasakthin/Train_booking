from app import create_app

app = create_app()  # Use the function from __init__.py


if __name__ == '__main__':
    app.run(debug=True)
