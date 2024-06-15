from datetime import timedelta,datetime
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
# this is a form that allows us to test user log in credentials
# the bearer token is a jwt, that will check with fastapi in the header before we process any request 
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from models import Users

#  a jwt needs a secret and an algorithm
from jose import jwt, JWTError

# jwt steps
# 1. (NEEDS TO BE A LONG STRING in the terminal type to generate a string -> openssl rand -hex 32  ) secret - 
SECRET_KEY = 'a254e76c2c008ae677f02996af60b6cb6b987d0f68edaaa9fa43a4a8912b5781'
# to create the signature we're missing the algorithm
ALGORITHM = 'HS256'

# libraries for our hashed password
# this encrypts and hashes passwords
from passlib.context import CryptContext
# instance of of cryptConext
# 2 params are required to use the library dont really need to know what they do - can look up for learning usual boiler plate code
bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated ='auto')
# tokenUrl param 
# contians the url that the client will send to our fast api application
#  we need this to verify the token as a dependency as token in our api request
# url -> auth/token, now when we check ou header we will see auth/token 
oauth2_bearer = OAuth2PasswordBearer(tokenUrl= 'auth/token')
'''
    In this app you could have multiple API routes, in this one we have an authication route
    the only one way to run this would be to turn off the main app, but then we would lose access to our main app
    end points, and so the way to deal with this is tell FastAPI, we have an extra route for x items in this case auth

    from this file we wxport auth routes to our main API file
'''
#  this is for decoding a JWT and later to verifying a user
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= 'Could not validate credentials')
        # if it does work return the user
        return {'username':username, 'id':user_id, 'user_role':user_role}
    except JWTError: 
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= 'Could not validate credentials')

    


# validation class - is active is auto made by the DB, and id is incremented by the ID
class CreateUserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str
    phone_number: str

class Token(BaseModel):
    access_token: str
    token_type: str


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
    # otherwise return the user that has been authenticated
    return user

# adding role to our jwt so that we can eval a user by also his/her role in the application
def create_access_token(username: str, user_id: int, role:str, expires_delta:timedelta):
    # 1. this is our encodeing that lives inside of the jwt which will contain information about the user
    encode = {'sub':username, 'id':user_id, 'role':role}
    #2. calculate when we want the jwt to expire & update our encoding  with the time we want for it to expire 
    expire = datetime.utcnow() + expires_delta
    encode.update({'exp':expire})
    # encode our JWT
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
    
     
# since password is hashed and thats diffrent from how we recieve it in our Db we can't dump the values they need to be opened up the password needs to be hashed and then we store the hash
    # to hash our password we need to install bcrpty
    # install seperately
    # pip install passlib
    # pip install bcrypt
    # hashed_password will equal whatever hash is return by bcrpt

# this divides our application in our Fast api to seperate our routes by category
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True,
        phone_number = create_user_request.phone_number,
    )
    db.add(create_user_model)
    db.commit()

# pip install python-multipart - will allow us to use a form from that libray that we install for authentication, swagger will have a feature to allow us to test for that
    
# takes our form and dependeny injection, and our db to test the validation
@router.post('/token', response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db:db_dependency):

    # grab the user, returns true or false
    user = authenticate_user(form_data.username, form_data.password, db)
    # if not true raise that we failed authenticate the user
    if not user: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= 'Could not validate credentials')


    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    # otherwise return the newly created token
    return {'access_token': token, 'token_type': 'bearer'}


@router.get('/users', status_code=status.HTTP_200_OK)
async def get_all_users(db:db_dependency):
    return db.query(Users).all()