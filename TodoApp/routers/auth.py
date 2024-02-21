from fastapi import APIRouter
from pydantic import BaseModel
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


# since password is hashed and thats diffrent from how we recieve it in our Db we can't dump the values they need to be opened up the password needs to be hashed and then we store the hash
    # to hash our password we need to install bcrpty
    # install seperately
    # pip install passlib
    # pip install bcrypt
    # hashed_password will equal whatever hash is return by bcrpt
router = APIRouter()
@router.post("/auth")
async def create_user(create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        is_active=True
    )
    return create_user_model