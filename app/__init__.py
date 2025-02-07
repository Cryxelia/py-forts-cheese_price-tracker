from flask import Flask
from database.config import Config
from app.routes import bp
from app.auth import login_manager, engine
from  database.models import Base, User, CheeseData, FavouriteProduct
from database.database import  SessionLocal


#retrives the user from the database
@login_manager.user_loader
def load_user(user_id):
    session = SessionLocal()
    user = session.get(User, int(user_id))  
    session.close()
    return user

#creates the app
def create_app():
    cheese_app = Flask(__name__)
    cheese_app.config.from_object(Config)
    
    login_manager.init_app(cheese_app)
    
    cheese_app.register_blueprint(bp)

    return cheese_app

