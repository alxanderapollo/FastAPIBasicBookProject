from database import Base
from sqlalchemy import Column, Integer, String, Boolean,ForeignKey

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)

#1. create a name for our DB with __tablename__
#2. after create our Cols,and determine if it is a PKey (qunique identifier), index = true allows our db to know that it is indexable 
class Todos(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default = False)
    owner = Column(Integer, ForeignKey("users.id"))