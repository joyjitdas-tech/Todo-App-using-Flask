from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.models import User
from app import db
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__)

# Root -> Registration page
@auth_bp.route('/')
def home():
    return redirect(url_for('auth.register'))

# REGISTER
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if User.query.filter_by(username=username).first():
            flash('Username already exists!', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('auth.login_page'))

    return render_template('register.html')

# LOGIN
@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('task.dashboard'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('auth.login_page'))

    return render_template('login.html')

# LOGOUT
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'success')
    return redirect(url_for('auth.login_page'))