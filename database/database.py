from database.config import Config
from sqlalchemy.orm import sessionmaker, declarative_base,scoped_session
from sqlalchemy import create_engine

#everything necesary to be able to create a database and the tables
Base = declarative_base()
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=True)

SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base.metadata.bind = engine