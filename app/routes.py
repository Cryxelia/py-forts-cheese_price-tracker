from flask import Blueprint, render_template, redirect, url_for, request, flash
from sqlalchemy import func
from database.models import  User, FavouriteProduct, CheeseData
from flask_login import login_user, login_required ,logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.database import SessionLocal
from service.cheese_service import get_cheese_statistics

bp = Blueprint('main', __name__)

@bp.route("/")
def get_mainpage():
    return render_template('index.html')

@bp.route("/cheese", methods=['GET'])
def cheese_page():
    session = SessionLocal()
    latest_dates = (  #retrieves the latest cheese prices in the database
    session.query(CheeseData.name,func.max(CheeseData.fetched_date).label("latest_date")).group_by(CheeseData.name).subquery())
    latest_cheeses = (session.query(CheeseData).join(latest_dates, (CheeseData.name == latest_dates.c.name) & (CheeseData.fetched_date == latest_dates.c.latest_date)).all())
    return render_template('cheese.html', cheeses=latest_cheeses)  

@bp.route("/loginview")
@login_required
def loginview(): 
    return render_template('loginview.html')

@bp.route("/login", methods=['GET', 'POST']) 
def login():
    session = SessionLocal()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = session.query(User).filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            session.close()
            return redirect(url_for('main.loginview'))
        else:
            flash('Invalid username or password')
            return redirect(url_for('main.login'))
    return render_template('login.html')

@bp.route('/register', methods=['GET', 'POST']) 
def register():
    session = SessionLocal()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if len(password) < 8:
            flash('Password must be at least 8 characters long.')
            return redirect(url_for('main.register'))
        if not any(c.islower() for c in password):
            flash('Password must include at least one lowercase letter.')
            return redirect(url_for('main.register'))
        if not any(c.isupper() for c in password):
            flash('Password must include at least one uppercase letter.')
            return redirect(url_for('main.register'))
        if not any(c.isdigit() for c in password):
            flash('Password must include at least one number.')
            return redirect(url_for('main.register'))
        if session.query(User).filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('main.register'))
        
        hashed_password = generate_password_hash(password,method='scrypt', salt_length=16)
        new_user = User(username=username, password=hashed_password)
        session.add(new_user)
        session.commit()
        flash('Registration successful! Please log in.')
        session.close()
        return redirect(url_for('main.login'))
    return render_template('register.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.get_mainpage'))

@bp.route("/all_cheese_login")
@login_required
def all_cheese_login():
    session = SessionLocal()
    latest_dates = (
    session.query(CheeseData.name,func.max(CheeseData.fetched_date).label("latest_date")).group_by(CheeseData.name).subquery())
    latest_cheeses = (session.query(CheeseData).join(latest_dates, (CheeseData.name == latest_dates.c.name) & (CheeseData.fetched_date == latest_dates.c.latest_date)).all())
    return render_template('all_cheeses_login.html', cheeses=latest_cheeses)  


@bp.route("/add_to_favourites/<int:cheese_id>", methods=['POST'])
@login_required
def add_to_favourites(cheese_id):
    session = SessionLocal()
    cheese = session.query(CheeseData).get(cheese_id)
    if not cheese:
        flash('Cheese not found!','error')
        return redirect(url_for('main.all_cheese_login'))
    existing_favourite = session.query(FavouriteProduct).filter_by(user_id=current_user.id, cheese_id=cheese.id).first()
    if existing_favourite:
        flash(f'{cheese.name} is already in your favourite cheese')
    else:
        favourite = FavouriteProduct(user_id=current_user.id, cheese_id=cheese.id)
        session.add(favourite)
        session.commit()
        flash(f'{cheese.name} has been added to your favourite cheese!')
    return redirect(url_for('main.all_cheese_login'))

@bp.route("/favourites") 
@login_required
def favourites():
    session = SessionLocal()
    favourite_cheeses = session.query(FavouriteProduct).filter_by(user_id=current_user.id).all()
    return render_template('favourites.html', cheeses=favourite_cheeses)

@bp.route('/delete_favourites/<int:favourite_id>', methods=['POST']) 
@login_required
def remove_favourite(favourite_id):
    session = SessionLocal()
    favourite = session.query(FavouriteProduct).filter_by(id=favourite_id, user_id=current_user.id).first()
    if favourite:
        session.delete(favourite)
        session.commit()
        flash(f'Cheese {favourite.cheese_id} has been removed from your favourites!', 'success')
    else:
        flash('Favourite not found!', 'error')
    return redirect(url_for('main.favourites'))

@bp.route('/all_cheese_login/<cheese_name>/prices')
@login_required
def cheese_statistics_main(cheese_name):
    return get_cheese_statistics(cheese_name)


@bp.route('/favourites/<cheese_name>/prices')
@login_required
def cheese_statistics_favourites(cheese_name):
    return get_cheese_statistics(cheese_name)