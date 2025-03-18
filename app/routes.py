import mysql.connector
from flask import Blueprint, request, jsonify ,redirect, url_for, flash, render_template, session, g
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash ,generate_password_hash
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError  # ✅ Correct import
from datetime import datetime
from .db_utils import get_train_data
import random
import string
from . import db  
from .models import Booking
from .models import Booking, Passenger, Train,TrainSeats, User, BookingPassenger, UserAccounts 

# Define Blueprint
main = Blueprint('main', __name__)


def get_train_data(train_id):
    return db.session.query(Train).filter(Train.train_id == train_id).first()

# Generate unique PNR number
def generate_pnr():
    return str(random.randint(1000000000, 9999999999)) 

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')  # 🔹 Ensure 'username' is retrieved
        email = request.form.get('email')
        password = request.form.get('password')

        if not username or not email or not password:
            flash("Please fill all fields.", "danger")
            return redirect(url_for('main.register'))

        # Check if user exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash("User already exists. Try a different username or email.", "warning")
            return redirect(url_for('main.register'))

        # Hash password before storing
        hashed_password = generate_password_hash(password)

        # ✅ Pass all required fields to the User model
        new_user = User(username=username, email=email, password_hash=hashed_password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('main.login'))  # ✅ Redirect to login
        except IntegrityError:
            db.session.rollback()
            flash("Database error. Please try again.", "danger")
            return redirect(url_for('main.register'))

    return render_template('register.html')  # Ensure this template exists


@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # ✅ Query the database using SQLAlchemy ORM
        user = User.query.filter_by(email=email).first()

        if user:
            # ✅ Compare entered password with stored hashed password
            if check_password_hash(user.password_hash, password):
                session['user_id'] = user.id  # ✅ Store user ID in session
                session['username'] = user.username  # (Optional) Store username
                flash("Login successful!", "success")
                return redirect(url_for('main.dashboard'))  # ✅ Redirect to dashboard
            else:
                flash("Incorrect password. Please try again.", "danger")
        else:
            flash("Email not found! Please register first.", "danger")

    return render_template('login.html')  # ✅ Render the login page


@main.route('/dashboard')
def dashboard():
    if 'user_id' not in session:  # ✅ Now it correctly checks for session['user_id']
        flash("❌ Please log in first!", "danger")
        return redirect(url_for('main.login'))

    user_id = session['user_id']
    
    # ✅ Fetch user details using SQLAlchemy
    user = User.query.filter_by(id=user_id).first()

    # ✅ Fetch all trains using SQLAlchemy
    trains = Train.query.all()

    if not user:
        flash("❌ User not found!", "danger")
        return redirect(url_for('main.login'))

    return render_template('dashboard.html', user=user, trains=trains)

@main.route('/book_ticket/<int:train_id>', methods=['GET', 'POST'])
def book_ticket(train_id):
    # Fetch train details from the database
    train = Train.query.filter_by(train_id=train_id).first()
    
    if not train:
        return "Train not found", 404  # Return error if train does not exist
    
    if request.method == 'POST':
        departure = request.form['departure']
        destination = request.form['destination']
        travel_date = request.form['travel_date']
        ticket_class = request.form['ticket_class']
        passenger_names = request.form.getlist('passenger_name[]')
        passenger_ages = request.form.getlist('passenger_age[]')
        passenger_genders = request.form.getlist('passenger_gender[]')
        passenger_id_proofs = request.form.getlist('passenger_id_proof[]')
        
        # Debugging: Print data to check if values are received
        print("Received Data:")
        print(f"Train ID: {train_id}, Train Name: {train.train_name}")
        print(f"Departure: {departure}, Destination: {destination}, Date: {travel_date}")
        print(f"Passengers: {passenger_names}")

        pnr = generate_pnr()  # ✅ Generate a single PNR for the whole booking
        
        print(f"Generated PNR: {pnr}")  # Debugging

        for i in range(len(passenger_names)):
            new_booking = BookingPassenger(
                train_id=train_id,
                train_name=train.train_name,
                departure=departure,
                destination=destination,
                travel_date=travel_date,
                class_type=ticket_class,
                passenger_name=passenger_names[i],
                age=passenger_ages[i],
                gender=passenger_genders[i],
                id_proof=passenger_id_proofs[i],
                pnr=pnr
            )
            db.session.add(new_booking)
        
        db.session.commit()  # Commit all entries
        
        return redirect(url_for('main.view_ticket', train_id=train_id, pnr=pnr))  # Redirect after booking confirmation
    
    return render_template('book_ticket.html', train=train) 

@main.route("/view_ticket")
def view_ticket():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="Selv@123", database="train_booking")
        cursor = conn.cursor(dictionary=True)

        # Fetch latest ticket with correct PNR
        cursor.execute("SELECT * FROM booking_passenger ORDER BY id DESC LIMIT 1")
        ticket = cursor.fetchone()  

        cursor.close()
        conn.close()

        if ticket:
            print("Ticket fetched:", ticket)  # Debugging
            return render_template("view_ticket.html", ticket=ticket)
        else:
            return render_template("view_ticket.html", ticket=None)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Database connection error!"


@main.route('/seat_availability')
def seat_availability():
    seat_data = db.session.query(
        TrainSeats.train_id,
        Train.train_name,
        TrainSeats.class_type,
        TrainSeats.upper_berth,
        TrainSeats.middle_berth,
        TrainSeats.lower_berth
    ).join(Train, TrainSeats.train_id == Train.train_id).all()  # Joining with Train table

    return render_template('seat_availability.html', seat_data=seat_data)

@main.route('/bookings')
def bookings():
    try:
        bookings = BookingPassenger.query.order_by(BookingPassenger.travel_date.desc()).all()
        return render_template('bookings.html', bookings=bookings)
    except Exception as e:
        flash(f"❌ Error fetching bookings: {str(e)}", "danger")
        return redirect(url_for('main.dashboard'))

@main.route('/cancel_ticket', methods=['GET','POST'])
def cancel_ticket():
    if request.method == 'POST':
        passenger_name = request.form.get('name')  # ✅ Use passenger_name
        id_proof = request.form.get('id_proof')

        # ✅ Check if passenger exists in `booking_passenger` table
        passenger = BookingPassenger.query.filter_by(passenger_name=passenger_name, id_proof=id_proof).first()

        if passenger:
            db.session.delete(passenger)  # ✅ Delete the entry
            db.session.commit()
            flash("Ticket canceled successfully!", "success")
        else:
            flash("No matching ticket found!", "danger")

    return render_template("cancel_ticket.html")


@main.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    flash("✅ You have been logged out.", "info")
    return redirect(url_for('main.login'))
