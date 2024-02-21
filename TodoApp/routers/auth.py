from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
# this is a form that allows us to test user log in credentials
from fastapi.security import OAuth2PasswordRequestForm


from models import Users

# libraries for our hashed password
# this encrypts and hashes passwords
from passlib.context import CryptContext

# instance of of cryptConext
# 2 params are required to use the library dont really need to know what they do - can look up for learning usual boiler plate code
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated ='auto')

'''
    In this app you could have multiple API routes, in this one we have an authication route
    the only one way to run this would be to turn off the main app, but then we would lose access to our main app
    end points, and so the way to deal with this is tell FastAPI, we have an extra route for x items in this case auth

    from this file we wxport auth routes to our main API file
'''
 
# validation class - is active is auto made by the DB, and id is incremented by the ID
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str


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


# function to authenticate our user
def authenticate_user(username: str, password: str, db: db_dependency):
    # 1.get all of the users from the User DB, and then filter by username, grabbing the first response
    user = db.query(Users).filter(Users.username == username).first()
    # 1A - if not user was ontained return False
    if not user: return False
    # 2 verify that we have the correct hashed password by using bcrypt to hash the password and check what we have in the Db if its not a match then return false
    if not bcrypt_context.verify(password, user.hashed_password): return False
    # otherwise return true we have the correct password
    return True
     


# since password is hashed and thats diffrent from how we recieve it in our Db we can't dump the values they need to be opened up the password needs to be hashed and then we store the hash
    # to hash our password we need to install bcrpty
    # install seperately
    # pip install passlib
    # pip install bcrypt
    # hashed_password will equal whatever hash is return by bcrpt
router = APIRouter()
@router.post("/auth", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    db.add(create_user_model)
    db.commit()

# pip install python-multipart - will allow us to use a form from that libray that we install for authentication, swagger will have a feature to allow us to test for that
    
# takes our form and dependeny injection, and our db to test the validation
@router.post('/token')
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):

    # grab the user, returns true or false
    user = authenticate_user(form_data.username, form_data.password, db)
    # if not true we failed
    if not user: return 'Failed Authentication'
    # otherwise return true
    return 'successful authentication'