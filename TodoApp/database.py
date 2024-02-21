# sql alchamey ORM (Object Relational Mapper), fast api use this to create a DB and connect to our DB 

from sqlalchemy import create_engine
# for our Db session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# Steps for Creating a DB with SQL lit

# 1.create a URL and directory for where the DB should live

# this is URL creates a location of this DB on our FAST API application
# in other words our DB will be in this directory inside of our TODO APP
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todosapp.db'
# 2. Create a DB Engine - allows us to open up a connection and let folks use our DB
    # look above for our import create_engine

# 3. create a varaible of that engine & add the URL path we create above
    # 3A. connect_args are args we pass into our create engine that allow us to define some kind of connection to our DB
    #3B.  'check same thread': false - SQL Lite only allow us to connect to one thread by default - this is to assume that each thread will handle an independent request, this is prevent an accident sharing with diffrent requests, but fast api is normal to use more than one thread at any one time  

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
# 4. session local - each instance of the seesion local will have a db session, now we create an instance 
# 4a. bind to the engine we just created, want to make sure our auto commits and auto flashes are false so that we have full control of the DB
SessionLocal = sessionmaker(autocommit=False, autoflush= False, bind=engine)
# 5 later on we want to call our db file, and create base which is obj of the Db which will then control the DB - with this we can create tables, and then we can create an obj of our db so we can interact with our DB in the future
Base = declarative_base()