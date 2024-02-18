# our table
from fastapi import FastAPI, Depends
# depends is dependency injection, we need to do something before we excute what we execute
# import our engine and our models
import models
from models import Todos
from database import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session

app = FastAPI()
# creates everything from our models file, and Db file to create a new DB with Todos and all of the columns that have been layed out
# only runs if our todo.db does not exist
models.Base.metadata.create_all(bind=engine)

# Db Dependency

def get_db():
    db = SessionLocal()
    # try yeild - only the code prior to and including the yeild statement is executed before sending the response 
    # finally the code is exceuted after the response has been delivered
    # ultimately allows us to contact the DB
    # yeild retuns all the information back
    try:
        yield db
    finally:
        db.close()
    
#  we can pass this varaible around to open up our api end point connection to our Db as Dependency injection, instead of writing a long list, fo
db_dependency = Annotated[Session, Depends(get_db)]

# annotated is from typing, session
# return db.query takes our models of todos, and returns all of the items inside 
@app.get("/")
async def read_all(db:db_dependency):
    return db.query(Todos).all()