from . import db
from sqlalchemy import Column, Integer, String  
from datetime import datetime
from werkzeug.security import generate_password_hash

class UserAccounts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

    def __repr__(self):
        return f"<UserAccounts {self.username}>"


class Passenger(db.Model):
    __tablename__ = 'passengers_info'  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    id_proof = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

class User(db.Model):
    __tablename__ = 'users'  

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)  # Unique
    email = db.Column(db.String(100), unique=True, nullable=False)  # Unique
    password_hash = db.Column(db.String(200), nullable=False)
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

class BookingPassenger(db.Model):
    __tablename__ = 'booking_passenger'

    id = db.Column(db.Integer, primary_key=True)
    train_id = db.Column(db.Integer, db.ForeignKey('trains.train_id'), nullable=False)
    train_name = db.Column(db.String(100), nullable=False)
    departure = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    class_type = db.Column(db.String(50), nullable=False)
    passenger_name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    id_proof = db.Column(db.String(20), nullable=False)
    pnr = db.Column(db.String(10), unique=True, nullable=False)

  
class Train(db.Model):
    __tablename__ = 'trains'  

    train_id = db.Column(db.Integer, primary_key=True)
    train_name = db.Column(db.String(100), nullable=False)
    departure_time = db.Column(db.Time, nullable=False)
    arrival_time = db.Column(db.Time, nullable=False)
    train_number = db.Column(db.String(10))
    source = db.Column(db.String(50))
    destination = db.Column(db.String(50))
    fare = db.Column(db.Numeric(10, 2))
    
    bookings = db.relationship('BookingPassenger', backref='train', lazy=True)



    def __repr__(self):
        return f"<Train {self.train_id} - {self.train_name}>"

class TrainSeats(db.Model):
    __tablename__ = 'train_seats'
    id = db.Column(db.Integer, primary_key=True)
    train_id = db.Column(db.Integer, db.ForeignKey('trains.train_id'), nullable=False)  # Update foreign key
    class_type = db.Column(db.Enum('AC', 'Non-AC'), nullable=False)
    upper_berth = db.Column(db.Integer, nullable=False)
    middle_berth = db.Column(db.Integer, nullable=False)
    lower_berth = db.Column(db.Integer, nullable=False)

    train = db.relationship('Train', backref=db.backref('seats', lazy=True))


class Booking(db.Model):
    __tablename__ = 'bookings'  # ✅ Explicit table name

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    train_id = db.Column(db.Integer, db.ForeignKey('trains.train_id'), nullable=False)
    train_name = db.Column(db.String(100), nullable=False)
    departure = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    travel_date = db.Column(db.Date, nullable=False)
    ticket_class = db.Column(db.String(50), nullable=False)
    pnr = db.Column(db.String(20), unique=True, nullable=False)
    passenger_count = db.Column(db.Integer, nullable=False)
    id_proof = db.Column(db.String(50), nullable=False)  # ✅ New column for ID proof
 
    def __repr__(self):
        return f"<Booking {self.id} - PNR: {self.pnr}>"

