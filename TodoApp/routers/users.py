'''
    this api route is for our users 
    it gets users by email and returns the requested information after making sure the requeste has been verified

    and it updates the user password, using bcrypt to hash and then stores it into the db 

'''




#DB Stuff 
# DB models for creating users, and getting all of our users
from models import Users
# this import is where our db lives and is created, and connected, this is how we use it in our project
from database import SessionLocal
from sqlalchemy.orm import Session
# ss
# FASTAPI and its libraries
# APIRouter -  for better structuring of our multiple API's across the project  
# Depends is used for our dependencies when we call on our DB
# HTTPEXCEPTIONS are for web exceptions, and status is for codes after commit a transaction 
from fastapi import APIRouter, Depends, HTTPException
from pydantic import Field, BaseModel
from typing import Annotated
from starlette import status

# from pur auth file import get_current_user function for verfication purposes
from .auth import get_current_user
# for encrypting our password when a fresh one is created
from passlib.context import CryptContext
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated ='auto')


router = APIRouter(
    tags=['users']
)

# for fetching our db during the session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# dependecies 
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# for verifying our pass and making sure that its at least a length of 6 characters
class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


# request to get user by email
# 3 params, user, db and user email
# 1. we verify the user exists by asking to log in
# 2. once verified successfully  - the user is asked to provide an email  
@router.get('/user/{email}', status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency, db:db_dependency, user_email:str ):
    # if the user doesnt exist throw a 400
    if user is None: raise HTTPException(status_code=401, detail='Authentication Failed')
    # search users db for a match email and return the first instance of it
    user_model = db.query(Users).filter(Users.email == user_email).first()
    # if the email is found return the user to the requeste 
    if user_model is not None: return user_model
    # otherwise let the user know we have not found the user 
    raise HTTPException(status_code = 404, detail='User not found')

# updating password
# 1. find user by email and retrive the user by id
# using the user verfication class to make sure our password is passing secruity measures
@router.put('/user/{email}', status_code=status.HTTP_200_OK)
async def update_password(user:user_dependency, db:db_dependency, user_verification: UserVerification):

    if user is None: raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    # if the passwords dont match, raise an exception
    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password Change')
    
    # otherwise add the new pass as an updated pass to our user - and then add that user
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()

@router.put('/phonenumber/{phone_number}', status_code=status.HTTP_200_OK)
async def update_phone_number(user:user_dependency, db:db_dependency,phone_number: str):

    if user is None: raise HTTPException(status_code=401, detail='Authentication Failed')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()






    
