from sqlalchemy.orm import scoped_session, sessionmaker
from flask_login import LoginManager
from database.database import engine

#everything necesary to login and open the app
login_manager = LoginManager()
login_manager.login_view = 'login'

session_factory = sessionmaker(bind=engine)
db_session = scoped_session(session_factory)