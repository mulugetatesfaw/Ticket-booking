#!/usr/bin/python3
from flask import Blueprint, flash, redirect, url_for, request
from models import storage
from models.bus import Bus
from models.admin import Admin
from flask import Flask, render_template, request, redirect, url_for, session

from flask import Flask, request
from models.route import Route
from models.city import City
from models.ticket import Ticket
from models.comment import Fedback
from models.user import User
from flask import Flask, render_template
from flask_login import current_user, login_user
from uuid import uuid4
from hashlib import md5
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash
views = Blueprint('views', __name__)

from flask import Flask, render_template
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.after_request
def add_no_cache_header(response):
    response.headers['Cache-Control'] = 'no-store'  # Set the Cache-Control header to 'no-store'
    return response

from flask import Blueprint, render_template, request, flash, redirect, url_for
from uuid import uuid4

from models import storage
from models.user import User
from hashlib import md5
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint("auth", __name__)

cache_id = str(uuid4())

@auth.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == "POST":
        data = request.form
        username = data.get('username')
        password = md5(data.get('password').encode()).hexdigest()
        users = storage.all(User).values()
        user = None
        for u in users:
            if u.username == username:
                user = u
                break
        if user:
            if password == user.password:
                flash("Logged in successfully", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.profile'))
            else:
                flash("Incorrect Password", category='error')
        else:
            flash("Incorrect username", category='error')
    return render_template("login.html", cache_id=cache_id, user=current_user)




@views.route('/root')
def root():
    return render_template('checkroot.html', route=route)
@app.route('/users/<string:email>')
def get_user(email):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE first_name=?", (email,))
    result = c.fetchone()
    conn.close()

    if result:
        user = {'id': result[0], 'fnam': result[1], 'lname': result[2], 'email': result[3]}
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404

@views.route('/ticket_number')
def ticket_number():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tickets')
    tickets = cursor.fetchall()
    for ticket in tickets:
        conn.close()
    return render_template('ticket.html', tickets=tickets)
# Define a route to display all users
@views.route('/users')
def users():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    if users:
        return render_template('users.html', users=users)
    else:
        return render_template('error.html', error="There is No user!!")

@views.route('/comments')
def comments():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM comments')
    comments  = cursor.fetchall()
    conn.close()
    if comments:
        return render_template('comments.html', comments=comments)
    else:
        return render_template('error.html', error="There is No Comment !!.")

@views.route('/routes')
def routes():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM routes')
    routes  = cursor.fetchall()
    conn.close()
    """
    routes = []
    buses = storage.all(Admin)
    for bus in buses.values():
        routes.append(bus.to_dict())
    """
    if routes:
        return render_template('routes.html', routes=routes)
    else:
        return render_template('error.html', error="There is No routes")
@views.route('/selectbus')
def selectbus():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM buses')
    data  = cursor.fetchall()
    for bus in data:
        conn.close()
    return render_template('route.html', data=data)
@views.route('/buses')
def buses():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM buses')
    buses  = cursor.fetchall()
    conn.close()
    if buses:
        return render_template('buses.html', buses=buses)
    else:
        return render_template('error.html',error="There is No Buses!")


@views.route('/home')
@views.route('/')
def home():
    raw_cities = storage.all(City)
    des = [city.to_dict() for city in raw_cities.values()]
    return render_template('index.html', des=des,user=current_user)

@views.route('/about')
def about():
    return render_template('about.html', user=current_user)

@views.route('/offers')
def offers():
    raw_cities = storage.all(City)
    des = [city.to_dict() for city in raw_cities.values()]
    return render_template('cheeckrout.html',des=des, user=current_user)

"""
@views.route('/ticket', methods=['GET', 'POST'], strict_slashes=False)
@views.route('/ticket')
def ticket():
    if request.method == 'POST':
        users = storage.all(Ticket).values()
        data = request.form
        print(data)
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        depcity = data.get('depcity')
        descity = data.get('descity')
        price = data.get('price')
        no_seat = data.get('no_seat')
        side_no = data.get('side_no')
        date = data.get('date')
        plate_no = data.get('plate_no')
        phone = data.get('phone')
    if len(phone) != 10:
        return render_template('ticket.html', error="phone must be 10 digit!")
    elif not no_seat.isdigit():
        return render_template('ticket.html', error="Incorrect This Bus is Full!")
    else:
        info = {
            "firstname": firstname,
            "lastname": lastname,
            "depcity": depcity,
            "descity": descity,
            "phone": phone,
            "date": date,
            "price": price,
            "no_seat": no_seat,
            "side_no": side_no,
            "plate_no": plate_no
        }
        new_account = Ticket(**info)
        new_account.save()
        return render_template('ticket.html',user=current_user, info=info, success="Ticket Booked Successfully!")

    return render_template('ticket.html',kery=kery, wenberkutr=wenberkutr, routes=routes, user=current_user)
"""
@views.route('/ticket', methods=['GET', 'POST'], strict_slashes=False)
def ticket():
    if request.method == 'POST':
        users = storage.all(Ticket).values()
        data = request.form
        print(data)
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        depcity = data.get('depcity')
        descity = data.get('descity')
        price = data.get('price')
        no_seat = data.get('no_seat')
        side_no = data.get('side_no')
        date = data.get('date')
        plate_no = data.get('plate_no')
        phone = data.get('phone')

        if len(phone) != 10:
            return render_template('ticket.html', error="Phone number must be 10 digits!")
        elif not no_seat.isdigit():
            return render_template('ticket.html', error="Incorrect bus information! The bus is full.")
        else:
            info = {
                "firstname": firstname,
                "lastname": lastname,
                "depcity": depcity,
                "descity": descity,
                "phone": phone,
                "date": date,
                "price": price,
                "no_seat": no_seat,
                "side_no": side_no,
                "plate_no": plate_no
            }
            new_account = Ticket(**info)
            new_account.save()
            return render_template('ticket.html', user=current_user, info=info, success="Ticket booked successfully!")
        return render_template('ticket.html')

"""
from telebirr import Telebirr
telebirr_client = Telebirr(api_key='YOUR_API_KEY', api_secret='YOUR_API_SECRET')

@views.route('/ticket', methods=['GET', 'POST'], strict_slashes=False)
def ticket():
    if request.method == 'POST':
        users = storage.all(Ticket).values()
        data = request.form
        print(data)
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        depcity = data.get('depcity')
        descity = data.get('descity')
        price = data.get('price')
        no_seat = data.get('no_seat')
        side_no = data.get('side_no')
        date = data.get('date')
        plate_no = data.get('plate_no')
        phone = data.get('phone')

        if len(phone) != 10:
            return render_template('ticket.html', error="Phone number must be 10 digits!")
        elif not no_seat.isdigit():
            return render_template('ticket.html', error="Incorrect bus information! The bus is full.")
        else:
            # Calculate the total amount to be paid
            total_amount = int(price) * int(no_seat)

            # Generate a payment reference ID or use your own unique identifier
            payment_reference = generate_payment_reference()

            # Create a payment request with the necessary details
            payment_request = {
                'amount': total_amount,
                'phone': phone,
                'reference': payment_reference,
                'description': 'Ticket Payment'
            }

            # Initiate the payment with Telebirr
            try:
                payment_response = telebirr_client.initiate_payment(payment_request)

                # Check if the payment initiation was successful
                if payment_response['status'] == 'SUCCESS':
                    # Store the payment reference and other ticket details in your database
                    info = {
                        "firstname": firstname,
                        "lastname": lastname,
                        "depcity": depcity,
                        "descity": descity,
                        "phone": phone,
                        "date": date,
                        "price": price,
                        "no_seat": no_seat,
                        "side_no": side_no,
                        "plate_no": plate_no,
                        "payment_reference": payment_reference
                    }
                    new_account = Ticket(**info)
                    new_account.save()

                    # Render the ticket page with success message
                    return render_template('ticket.html', user=current_user, info=info, success="Ticket booked successfully! Proceed with payment.")

                # If the payment initiation failed, render the ticket page with an error message
                return render_template('ticket.html', error="Payment initiation failed. Please try again.")

            except Exception as e:
                # Handle any exceptions that occurred during the payment initiation
                return render_template('ticket.html', error="An error occurred while initiating the payment.")
    return render_template('ticket.html')

"""
@views.route('/businsert', methods=['GET', 'POST'], strict_slashes=False)
@views.route('/businsert')
def businsert():
    if request.method == 'POST':
        buses = storage.all(Bus).values()
        plate_nos = [user.plate_no for user in buses]
        sidenos = [user.sideno for user in buses]
        no_seatss = [user.no_seats for user in buses]
        data = request.form
        print(data)
        plate_no = data.get('plate_no')
        sideno = data.get('sideno')
        no_seats = data.get('no_seats')


        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM buses WHERE plate_no = ?", (plate_no,))
        bus = c.fetchall()         
        conn.close()


        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM buses WHERE sideno = ?", (sideno,))
        side_no = c.fetchall()
        conn.close()
        if bus:
            return render_template('Businsert.html', error="plate Number is already Exist!")
        elif side_no:
            return render_template('Businsert.html', error="side Number is already Exist!")
        else:
            info = {"plate_no": plate_no, "sideno": sideno, "no_seats": no_seats}
            new_account = Bus(**info)
            new_account.save()
            return render_template('Businsert.html', success=" Bus Registored Successfully")
    return render_template('Businsert.html', user=current_user)

@views.route('/comment', methods=['GET', 'POST'], strict_slashes=False)
@views.route('/comment')
def comment():
    if request.method == 'POST':
        coments = storage.all(Fedback).values()
        names = [user.name for user in coments]
        messages = [user.message for user in coments]
        emails = [user.email for user in coments]
        phones = [user.phone for user in coments]
        data = request.form
        print(data)
        message = data.get('message')
        email = data.get('email')
        phone = data.get('phone')
        name = data.get('name')
        if email in emails:
            flash("email is already existed", category="error")
        else:
            info = {"message": message, "email": email, "phone": phone, "name": name}
            new_account = Fedback(**info)
            new_account.save()

            return render_template('comment.html', success="comment successfully submitted!!")
    return render_template('comment.html', user=current_user)

@views.route('/get_ticket', methods=['GET', 'POST'], strict_slashes=False)
def get_ticket():
    raw_cities = storage.all(City)
    des = [city.to_dict() for city in raw_cities.values()]

    if request.method == 'POST':
        depcity = request.form.get('depcity')  # Get the value of 'depcity' from the form or request data
        descity = request.form.get('descity')
        date = request.form.get('date')
        firstname = request.form.get('firstname')
        lastname = request.form.get('lastname')

    
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM tickets WHERE depcity = ? AND descity = ? AND date = ? AND firstname = ? AND lastname = ?", (depcity, descity, date, firstname, lastname))
        ticket = c.fetchall()
        conn.close()
        if ticket:
            return render_template('tickets.html', ticket=ticket, success="Your Ticket is:")
        elif depcity == descity:
             return render_template('error1.html', error="Try Again. Entered Departure and Destination is the Same!")
        elif firstname == lastname:
            return render_template('error1.html', error="Try Again. Entered Firestname AND Lastname The Same!")

        else:
            return render_template('error1.html', error="Try Again. There is no Ticket Booked info for the entered details!")
    return render_template('getticket.html', des=des)

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

@app.route('/distance', methods=['POST'])
def distance():
    city1 = request.form['city1']
    city2 = request.form['city2']

    geolocator = Nominatim(user_agent="city_distance_app")
    location1 = geolocator.geocode(city1)
    location2 = geolocator.geocode(city2)
    if location1 is None or location2 is None:
        return render_template('route.html', error='Invalid city name(s) entered.')
    distance = geodesic((location1.latitude, location1.longitude), (location2.latitude, location2.longitude)).kilometers
    return render_template('route.html', distance=distance)
@views.route('/route', methods=['GET', 'POST'], strict_slashes=False)
@views.route('/route')
def route():
    raw_cities = storage.all(City)
    des = [city.to_dict() for city in raw_cities.values()]
    data = []
    buses = storage.all(Bus)
    for bus in buses.values():
        data.append(bus.to_dict()) 
    if request.method == 'POST':
        data = request.form
        routes = storage.all(Route).values()
        plate_nos = [route.plate_no for route in routes]
        side_nos = [route.side_no for route in routes]
        departure = [route.depcity for route in routes]
        desparture = [route.descity for route in routes]
        dates = [route.date for route in routes]

        print(data)

        descity = data.get('descity')
        depcity = data.get('depcity')
        kilometer = data.get('kilometer')
        plate_no = data.get('plate_no')
        side_no = data.get('side_no')
        price = data.get('price')
        date = data.get('date')
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM routes WHERE date=? AND depcity=? AND descity=? AND plate_no=?", (date, depcity, descity, plate_no))
        rout = cursor.fetchone()


        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM routes WHERE date=? AND plate_no=? AND side_no=?", (date, plate_no, side_no))
        bus = cursor.fetchone()

        cursor.execute("SELECT * FROM routes WHERE date=? AND plate_no=?", (date, plate_no))
        same_date = cursor.fetchone()
        
        if same_date:
            data = []
            buses = storage.all(Bus)
            for bus in buses.values():
                data.append(bus.to_dict())
            return render_template('route.html', des=des, data=data, error="Bus is already  Reserved for other route!!")
        elif bus:
            data = []
            buses = storage.all(Bus)
            for bus in buses.values():
                data.append(bus.to_dict())
            return render_template('route.html', des=des, data=data, error="Bus is Reserved for other route!!")
        elif rout:
            data = []
            buses = storage.all(Bus)
            for bus in buses.values():
                data.append(bus.to_dict())
            return render_template('route.html', des=des, data=data, error="route already exists!!")
        elif depcity == descity:
            data = []
            buses = storage.all(Bus)
            for bus in buses.values():
                data.append(bus.to_dict())
            return render_template('route.html', data=data, des=des, error="Desparture and Destination the Same!!")
        else:
            info = {"depcity": depcity, "side_no": side_no, "price": price, "date": date, "descity": descity, "kilometer": kilometer, "plate_no": plate_no}
            new_account = Route(**info)
            new_account.save()
            
            data = []
            buses = storage.all(Bus)
            for bus in buses.values():
                data.append(bus.to_dict())
            return render_template('route.html', data=data,des=des, success="Route successfully submitted!")
    return render_template('route.html', des=des, data=data)

@views.route('/city', methods=['GET', 'POST'], strict_slashes=False)
@views.route('/city')
def city():
    if request.method == 'POST':
        data = request.form
        cities= storage.all(City).values()
        departure = [citiy.depcity for citiy in cities]
        depcity = data.get('depcity')
        if depcity in departure:
            return render_template('city.html', error="city already Exist!")
        else:
            info = {"depcity": depcity}
            new_account = City(**info)
            new_account.save()
            return render_template('city.html', success="City successfully registered!!")
    return render_template('city.html')

@views.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        users = storage.all(Admin).values()
        usernames = [user.username for user in users]
        emails = [user.email for user in users]
        phones = [user.phone for user in users]
        data = request.form
        print(data)
        email = data.get('email')
        fname = data.get('fname')
        lname = data.get('lname')
        password = data.get('password')
        phone = data.get('phone')
        gender = data.get('gender')
        username = data.get('username')
        if username in usernames:
            return render_template('admin.html',error="username already exist")
        elif email in emails:
            return render_template('admin.html',error="this email Already exist")
        elif len(password) < 6 or len(password) > 15:
            return render_template('admin.html', error="pasword must be 6 - 15 Characters length")
        elif len(phone) != 10:
            return render_template("admin.html", error="phone number must be equal to 10 digit")
        elif phone in phones:
            return render_template("admin.html", error="phone number already exist")
        else:
            info = {"fname": fname, "lname": lname,
                    "username": username, "password": password, "phone": phone, "gender": gender,
                    "email": email
                    }
            new_account = Admin(**info)
            new_account.save()
            login_user(new_account, remember=True)
            return render_template('admin.html', success="Admin successfully Registored!")
    return render_template("admin.html", user=current_user)
@views.route('/registor', methods=['GET', 'POST'], strict_slashes=False)
@views.route('/')
def registor():
    if request.method == 'POST':
        users = storage.all(User).values()
        usernames = [user.username for user in users]
        emails = [user.email for user in users]
        phones = [user.phone for user in users]
        data = request.form
        print(data)
        email = data.get('email')
        fname = data.get('fname')
        lname = data.get('lname')
        password = data.get('password')
        phone = data.get('phone')
        gender = data.get('gender')
        username = data.get('username')
        if username in usernames:
            return render_template('registor.html',error="email is already exist")
        elif email in emails:
            return render_template('registor.html', error="Email address already exists!")
        elif phone in phones:
            flash("Phone number already exists", category='error')
        else:
            info = {"fname": fname, "lname": lname,
                    "username": username, "password": password, "phone": phone, "gender": gender,  
                    "email": email
                    }
            new_account = User(**info)
            new_account.save()
            login_user(new_account, remember=True)
        return render_template('registor.html', success="User Registor Successfully!")
    return render_template("registor.html", user=current_user)    
@views.route('/ad')
@views.route('/')
def ad():
    return render_template('ad.html')
@views.route('/checkuser')
def checkuser():
    return render_template('checkuser.html')
@views.route('/get_user', methods=['GET', 'POST'])
def get_user():
    if request.method == 'POST':
        email = request.form['email']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email=?', (email,))
        users = cursor.fetchall()
        if users:
            for user in users:
                return render_template('userss.html', users=users)
        else:
            return render_template('checkuser.html')
    return render_template('checkuser.html')

@views.route('/get_route', methods=['GET', 'POST'])
def get_route():
    if request.method == 'POST':
        date = request.form['date']
        depcity = request.form['depcity']
        descity = request.form['descity']

        routes = []
        buses = storage.all(Route)
        for bus in buses.values():
            if bus.depcity == depcity and bus.descity == descity and bus.date == date:
                routes.append(bus.to_dict())
        raw_cities = storage.all(City)
        des = [city.to_dict() for city in raw_cities.values()]
        if routes:
            return render_template('checkroot.html', routes=routes, success="Routes info---")
        else:
            return render_template('index.html', des=des,error="Try Again There is no Route this info!")
    return render_template('cheeckrout.html',des=des)

@views.route('/book', methods=['GET', 'POST'])
def book():
    raw_cities = storage.all(City)
    des = [city.to_dict() for city in raw_cities.values()]
    if request.method == 'POST':
        date = request.form['date']
        depcity = request.form['depcity']
        descity = request.form['descity']
        raw_cities = storage.all(City)
        des = [city.to_dict() for city in raw_cities.values()]
        routes = []
        buses = storage.all(Route)
        for bus in buses.values():
            if bus.depcity == depcity and bus.descity == descity and bus.date == date:
                routes.append(bus.to_dict())
        if routes:
            return render_template('roote.html', routes=routes, success="Route info Goto Ticket page!! ")
        else:
            return render_template('cheeckroutee.html', des=des,error='There is no Travel in this city and date!')
    return render_template('cheeckroutee.html', des=des)
@views.route('/Select', methods=['GET', 'POST'])
def Select():
    if request.method == 'POST':
        plate_no = request.form['plate_no']
        depcity = request.form['depcity']
        descity = request.form['descity']
        date = request.form['date']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(no_seat) FROM tickets WHERE depcity = ? AND descity = ? AND date = ? AND plate_no = ?', (depcity, descity, date, plate_no))
        data = cursor.fetchall()
        count = data[0]
        conn.close()
        count_str = str(count)
        count_str = count_str.strip('(),')

        

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(no_seat) FROM tickets WHERE depcity = ? AND descity = ? AND date = ? AND plate_no = ?', (depcity, descity, date, plate_no))
        data = cursor.fetchall()
        count = data[0]
        conn.close()
        count_str = str(count)
        count_str = count_str.strip('(),')
    

        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(no_seat) FROM tickets WHERE depcity = ? AND descity = ? AND date = ? AND plate_no = ?', (depcity, descity, date, plate_no))
        seatnumber = cursor.fetchone()
        conn.close()
         
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM routes WHERE depcity = ? AND descity = ? AND date = ? AND plate_no = ?", (depcity, descity, date, plate_no))
        routes = c.fetchall()
        conn.close()
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT no_seats FROM buses WHERE plate_no = ?", (plate_no,))
        no_seat = c.fetchall()
        seat = no_seat[0]
        conn.close()
        seats = str(seat)
        seats = seats.strip('(),')
        seats = int(seats)
        count_str = int(count_str)
        
        numcount = seatnumber[0]
        wenberkutr = str(int(numcount))

        if seats <= 0:
            kery = 0
            wenberkutr = "full"
        else:
            kery = max(0, seats - count_str)

        if kery == 0:
            wenberkutr = "FULL"
        else:
            wenberkutr = str(int(wenberkutr) + 1)

        if routes:
            for route in routes:
                return render_template('ticket.html',kery=kery, wenberkutr=wenberkutr, routes=routes)
        else:
            return render_template('roote.html', error="do.nt ticket booked")
    return render_template('roote.html')
@views.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        current_password = request.form['password']
        new_password = request.form['new_password']
        if check_password(current_password):
            change_password_in_database(new_password)
            return 'Password changed successfully'
        else:
            return 'Current password is incorrect'
    else:
        return render_template('changepassword.html')

@views.route('/details')
def details():
    bus_id = request.args.get('id')
    bus = storage.get(Bus, bus_id)
    route_name = storage.get(Route, bus.route_id).name
    number_of_schedules = len(bus.schedules)
    return render_template('details.html',
                           user=current_user,
                           bus=bus,
                           route_name=route_name,
                           number_of_schedules=number_of_schedules)

@views.route('/admindelete')
def admindelete():
    admins = []
    buses = storage.all(Admin)
    for bus in buses.values():
        admins.append(bus.to_dict())

    return render_template('admindelet.html', admins=admins)


@views.route('/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        username = request.form['username']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM admins')
        row_count = cursor.fetchone()[0]
        
        if row_count <= 1:
            conn.close()
            admins = []
            buses = storage.all(Admin)
            for bus in buses.values():
                admins.append(bus.to_dict())

            return render_template('admindelet.html',admins=admins, error="Cannot delete admin. At least one account must exist.")

        cursor.execute('DELETE FROM admins WHERE fname=? AND lname=? AND username=?', (fname, lname, username))
        rows_deleted = cursor.rowcount
        conn.commit()
        conn.close()

        if rows_deleted > 0:
            admins = []
            buses = storage.all(Admin)
            for bus in buses.values():
                admins.append(bus.to_dict())
            return render_template('admindelet.html', admins=admins, success="Admin deleted successfully.")
        else:
            return render_template('admindelet.html', error="No admin found with the provided information.")

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM admins')
    admins = cursor.fetchall()
    conn.close()

    if admins:
        return render_template('admindelet.html', admins=admins)
    else:
        return render_template('error.html', error="There are no admins to delete.")
@views.route('/routedelete', methods=['GET', 'POST'])
def routedelete():
    if request.method == 'POST':
        depcity = request.form['depcity']
        descity = request.form['descity']
        date = request.form['date']
        plate_no = request.form['plate_no']
        side_no = request.form['side_no']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM routes WHERE depcity=? AND descity=? AND date=? AND plate_no=? AND side_no=?', (depcity, descity, date, plate_no, side_no))
        rows_deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
    
        routes = []
        cite = storage.all(Route)
        for city in cite.values():
            routes.append(city.to_dict())
        if rows_deleted > 0:
            return render_template('routedelete.html', routes=routes,success="Route Deleted Successfully!")
        else:
            return render_template('routedelete.html', routes=routes)
    routes = []
    cite = storage.all(Route)
    for city in cite.values():
        routes.append(city.to_dict())
    if routes:
        return render_template('routedelete.html', routes=routes, success="Route Deleted Successfully!")
    else:
        return render_template('error.html',error="There is No routes for Delete")
@views.route('/busdelete')
def busdelete():
    buses = []
    buse = storage.all(Bus)
    for bus in buse.values():
        buses.append(bus.to_dict())
    if buses:
        return render_template('busdelet.html', buses=buses)
    else:
        return render_template('error.html', error="NO buses for delete ")
@views.route('/deletebus', methods=['GET', 'POST'])
def deletebus():
    if request.method == 'POST':
        plate_no = request.form['plate_no']
        sideno = request.form['sideno']
        no_seats = request.form['no_seats']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM buses WHERE plate_no=? AND sideno=? AND no_seats=?', (plate_no, sideno, no_seats))
        rows_deleted = cursor.rowcount

        conn.commit()
        conn.close()
        buses = []
        buse = storage.all(Bus)
        for bus in buse.values():
            buses.append(bus.to_dict())
        if rows_deleted > 0:
            return render_template('busdelet.html', buses=buses, success="Bus Deleted Successfully!")
        else:
            return render_template('error.html',error="Error occured!")
@views.route('/citydelete', methods=['GET', 'POST'])
def citydelete():
    if request.method == 'POST':
        depcity = request.form['depcity']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cities WHERE depcity=?', (depcity,))
        rows_deleted = cursor.rowcount

        conn.commit()
        conn.close()
        cities = []
        cite = storage.all(City)
        for city in cite.values():
            cities.append(city.to_dict())
        if rows_deleted > 0:
            return render_template('citydelet.html', cities=cities,success="City Deleted Successfully")
        else:
            return render_template('citydelet.html', cities=cities,error="There is No city for Deleted")
    cities = []
    cite = storage.all(City)
    for city in cite.values():
        cities.append(city.to_dict())
    if cities:
         return render_template('citydelet.html', cities=cities)
    else:
        return render_template('error.html', error="There is No city for Delete")
@views.route('/commentdelete', methods=['GET', 'POST'])
def commentdelete():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM comments WHERE name=? AND email=? AND phone=?', (name, email, phone,))
        rows_deleted = cursor.rowcount

        conn.commit()
        conn.close()

        comments = []
        cite = storage.all(Fedback)
        for city in cite.values():
            comments.append(city.to_dict())
        if rows_deleted > 0:
            return render_template('commentdelet.html', comments=comments,success="comment deleted successfully!")
        else:
            return render_template('commentdelet.html',error="There is no Comment for Delete!")
    comments = []
    cite = storage.all(Fedback)
    for city in cite.values():
        comments.append(city.to_dict())
    if comments:
        return render_template('commentdelet.html', comments=comments)
    else:
        return render_template('error.html', error="NO Comments for delete!")


@views.route('/updatebus', methods=['POST', 'GET'])
def updatebus():
    if request.method == 'POST':
        plate_no = request.form['plate_no']
        sideno = request.form['sideno']
        no_seats = request.form['no_seats']
        new_sideno = request.form['new_sideno']


        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT sideno FROM buses WHERE sideno=?', (new_sideno,))
        existing_sideno = cursor.fetchone()
        if existing_sideno:
            buses = []
            buse = storage.all(Bus)
            for bus in buse.values():
                buses.append(bus.to_dict())
            return render_template('busupdate.html', buses=buses, error="The new sideno already exists.")
        cursor.execute('UPDATE buses SET sideno=? WHERE plate_no=? AND no_seats=? AND sideno=?',
                       (new_sideno, plate_no, no_seats, sideno))
        
        conn.commit()
        buses = []
        buse = storage.all(Bus)
        for bus in buse.values():
            buses.append(bus.to_dict())
        return render_template('busupdate.html', buses=buses, success="Side Number changed successfully!")

    buses = []
    buse = storage.all(Bus)
    for bus in buse.values():
        buses.append(bus.to_dict())
    if buses:
        return render_template('busupdate.html', buses=buses)
    else:
        return render_template('error.html', error="No buses for update")
@views.route('/profile')
def profile():
    return render_template('profile.html', user=current_user)
    if __name__ == '__main__':
        app.run(debug=True)
