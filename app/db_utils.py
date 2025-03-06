from flask_mysqldb import MySQL

mysql = MySQL()  # Ensure MySQL is initialized in `app.py`

def get_train_data(train_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM trains WHERE id = %s", (train_id,))
    train = cursor.fetchone()
    cursor.close()
    return train
