# our table
from fastapi import FastAPI
# import our engine and our models
import models
from database import engine

app = FastAPI()
# creates everything from our models file, and Db file to create a new DB with Todos and all of the columns that have been layed out
models.Base.metadata.create_all(bind=engine)