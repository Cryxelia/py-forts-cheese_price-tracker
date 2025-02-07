import os

#the app configurations
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY',  '4kjf7deem2o8e84hdbhzswuaw287sgh3te64u') 
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///cheeseapp.db') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    