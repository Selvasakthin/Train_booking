import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="your_mysql_password",  # Replace with your MySQL password
        database="train_booking"  # Change this to your actual database name
    )

    if conn.is_connected():
        print("✅ Connection Successful!")

    # Create a cursor object
    cursor = conn.cursor()

    # Execute a test query
    cursor.execute("SHOW TABLES;")

    print("Tables in the database:")
    for table in cursor.fetchall():
        print(table)

    # Close the connection
    conn.close()

except mysql.connector.Error as err:
    print(f"❌ Error: {err}")
