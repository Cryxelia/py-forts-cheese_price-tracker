from flask_login import UserMixin
from sqlalchemy import Column, Float, ForeignKey, Integer, String, DateTime
from database.database import Base
from sqlalchemy.orm import relationship


#models for the differente database tables
class User(UserMixin, Base):
    __tablename__ = 'user' #sets the tabel name
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(150),  unique=True, nullable=False, index=True)
    password = Column(String(150), nullable=False)
    favourites = relationship('FavouriteProduct', backref='owner', lazy=True)
    
    def get_id(self):
        return str(self.id)


class CheeseData(Base):
    __tablename__ = 'cheeseprices'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, index=True)
    price = Column(String(150), nullable=False)
    fetched_date = Column(DateTime, nullable=False)

    def __repr__(self):
        return f"<CheeseData(id={self.id}, name='{self.name}', price='{self.price}, fetched_date='{self.fetched_date}')>"


class FavouriteProduct(Base):
    __tablename__ = 'favourite_product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    cheese_id = Column(Integer, ForeignKey('cheeseprices.id'), nullable=False)
    cheese = relationship('CheeseData', backref='favourites')
    def __repr__(self):
        return f"<FavouriteProduct(id={self.id}, cheese_id={self.cheese_id}, cheese_name={self.cheese})>"
