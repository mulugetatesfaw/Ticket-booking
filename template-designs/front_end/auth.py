#!/usr/bin/python3
"""
file: views.py
Desc: A module responsible for handling all user authentication
Authors: Teklemariam Mossie, Mulugeta Tadege, and kidus Kinde
Date Created: sep 18 2023
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from uuid import uuid4

from models import storage
from models.user import User
from hashlib import md5
from flask_login import login_user, login_required, logout_user, current_user
import sqlite3


auth = Blueprint("auth", __name__)

cache_id = str(uuid4())

import hashlib

import hashlib

@auth.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Hash the password
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        # Check if user exists in the database based on username, password, and role
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        if role == 'user':
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
            user = c.fetchone()
            conn.close()

            if user:
                return render_template('profile.html', user=current_user)
            else:
                return render_template('login.html', error='Invalid username, password, or role')
        
        elif role == 'admin':
            c.execute("SELECT * FROM admins WHERE username = ? AND password = ?", (username, hashed_password))
            user = c.fetchone()
            conn.close()

            if user:
                return render_template('ad.html', user=user)
            else:
                return render_template('login.html', error='Invalid username, password, or role')
        
        else:
            return render_template('login.html', error='Invalid role')

    return render_template('login.html')

"""
@auth.route('/login', methods=['GET', 'POST'], strict_slashes=False)
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Hash the password
        hashed_password = hashlib.md5(password.encode()).hexdigest()

        # Check if user exists in the database
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_password))
        user = c.fetchone()
        conn.close()

        if user:
            return render_template('profile.html', user=current_user)
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')
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
"""

@auth.route('/logout', strict_slashes=False)
@login_required
def logut():
    logout_user()
    return redirect(url_for('auth.login'))
@auth.route('/sign-up', methods=['GET', 'POST'], strict_slashes=False)
def register():
    if request.method == 'POST':
        users = storage.all(User).values()
        usernames = [user.username for user in users]
        emails = [user.email for user in users]
        phone_numbers = [user.phone for user in users]
        data = request.form
        email = data.get('email')
        first_name = data.get('firstName')
        last_name = data.get('lastName')
        password1 = data.get('password1')
        password2 = data.get('password2')
        phone_number = data.get('phoneNumber')
        username = data.get('username')

        if username in usernames:
            flash("Username already exists", category="error")
        elif email in emails:
            flash("Email address already exists", category='error')
        elif len(password1) < 6 or len(password1) > 15:
            flash("Password must be 6 - 15 characters length",
                  category='error')
        elif password1 != password2:
            flash("Passwords don't match", category='error')
        elif len(phone_number) != 10:
            flash("Please insert a valid phone number", category='error')
        elif phone_number in phone_numbers:
            flash("Phone number already exists", category='error')
        else:
            info = {"first_name": first_name, "last_name": last_name,
                    "email": email, "phone": phone_number, "password": password1,
                    "username": username}
            new_account = User(**info)
            new_account.save()
            login_user(new_account, remember=True)
            flash("Account created successfully", category='success')
            return redirect(url_for('views.home'))

    return render_template("register.html", cache_id=cache_id, user=current_user)
