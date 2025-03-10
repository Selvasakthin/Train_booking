from flask_sqlalchemy import SQLAlchemy
import pymysql

pymysql.install_as_MySQLdb()
db = SQLAlchemy()

def get_train_data(train_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM trains WHERE id = %s", (train_id,))
    train = cursor.fetchone()
    cursor.close()
    return train
