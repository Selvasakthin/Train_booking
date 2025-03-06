from mains import db

try:
    with db.engine.connect() as connection:
        result = connection.execute("SELECT DATABASE();")
        print("Connected to:", result.fetchone()[0])
except Exception as e:
    print("Database connection failed:", str(e))
