from unicodedata import name
from flask import Flask, render_template, request, redirect, url_for, session, flash
from data.db_conn import db_auth
from services.account_service import create_user, login_user, get_profile
import os

app = Flask(__name__)

graph = db_auth()
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template('home/index.html')

@app.route('/accounts/register', methods=['GET'])
def register():
    return render_template('accounts/register.html')

@app.route('/accounts/register', methods=['POST'])
def register_post():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
    
    if password != confirm_password:
        flash('Passwords do not match')
        return render_template('accounts/register.html', email=email, first_name=first_name, last_name=last_name)
    if not name or not email or not password or not first_name or not last_name:
        flash('Please fill in all fields')
        return render_template('accounts/register.html', email=email, first_name=first_name, last_name=last_name)
    
    user = create_user(first_name, last_name, email, password)
    if not user:
        flash('Email already in use')
        return render_template('accounts/register.html', email=email, first_name=first_name, last_name=last_name)

    return redirect(url_for('login'))


@app.route('/accounts/login', methods=['GET'])
def login():
    if 'user_id' in session:
        return redirect(url_for('profile_get'))
    else:
        return render_template('accounts/login.html')


@app.route('/accounts/login', methods=['POST'])
def login_post():
    email = request.form['email']
    password = request.form['password']
    if not email or not password:
        flash('Please fill in all fields')
        return render_template('accounts/login.html')
    user = login_user(email, password)
    if not user:
        flash('Incorrect email or password')
        return render_template('accounts/login.html')
    
    user_id = request.form['email']
    session['user_id'] = user_id
    return redirect(url_for('profile_get'))

@app.route('/accounts/profile', methods=['GET'])
def profile_get():
    # Make sure the user has an active session.  If not, redirect to the login page.
    if "user_id" in session:
        user_id = session["user_id"]
        session['user_id'] = user_id
        user_profile = get_profile(user_id)
        return render_template("accounts/index.html", user_profile=user_profile)
    else:
        return redirect(url_for("login_get"))

@app.route('/accounts/profile', methods=['GET'])
def profile_post():
    # Make sure the user has an active session.  If not, redirect to the login page.
    if "user_id" in session:
        user_id = session["user_id"]
        session['user_id'] = user_id
        user_profile = get_profile(user_id)
        return render_template("accounts/index.html", user_profile=user_profile)
    else:
        return redirect(url_for("login_get"))

@app.route('/accounts/logout')
def logout():
    session.pop("usr", None)
    flash("You have successfully been logged out.", "info")
    return redirect(url_for("login_get"))


if __name__ == '__main__':
    app.run(debug=True)