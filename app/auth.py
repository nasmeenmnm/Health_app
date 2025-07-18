from flask import Blueprint, render_template, redirect, request, flash, url_for
from flask_login import login_user, logout_user, login_required
from .utils import get_user_by_username, add_user

auth = Blueprint('auth', __name__)
@auth.route('/')
def home():
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = get_user_by_username(username)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash("Invalid credentials")
    return render_template("login.html")


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
    


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        age = request.form['age']
        gender = request.form['gender']
        phoneno = request.form['phoneno']
        adress = request.form['adress']
        add_user(username, password, age, gender, phoneno, adress )
        return redirect(url_for('auth.login'))
    return render_template("register.html")
