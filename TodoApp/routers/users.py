from models import Users
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import Field, BaseModel
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated ='auto')


router = APIRouter(
    tags=['users']
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

    
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# for verifying our pass
class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


# get user
@router.get('/user/{email}', status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency, db:db_dependency, userEmail:str ):
    if user is None: raise HTTPException(status_code=401, detail='Authentication Failed')

    user_model = db.query(Users).filter(Users.email == userEmail).first()
    if user_model is not None: return user_model
    
    raise HTTPException(status_code = 404, detail='User not found')

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






    
