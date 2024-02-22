# our table
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
# depends is dependency injection, we need to do something before we excute what we execute
# import our engine and our models
from models import Todos
from database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status

router = APIRouter()
# creates everything from our models file, and Db file to create a new DB with Todos and all of the columns that have been layed out
# only runs if our todo.db does not exist
# models.Base.metadata.create_all(bind=engine)

# # to include api endpoints from our auth file 
# app.include_router(auth.router)

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

# validation for our todo request
# dont need to make an id bc fast api takes care of it
class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3,max_length=100)
    priority: int  = Field(gt=0,lt=6)
    complete: bool

# annotated is from typing, session
# return db.query takes our models of todos, and returns all of the items inside 
@router.get("/", status_code = status.HTTP_200_OK)
async def read_all(db:db_dependency):
    return db.query(Todos).all()

# return a match as soon as we see one
@router.get('/todo/{todo_id}', status_code = status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt = 0) ):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is not None: return todo_model
    raise HTTPException(status_code = 404, detail='Todo not found')

@router.post('/todo', status_code=status.HTTP_201_CREATED)
async def create_todo(db:db_dependency, todo_request:TodoRequest):
    todo_model= Todos(**todo_request.model_dump())

    '''.add() adds to the open DB sessions (think of it more like getting the database ready with some data.)
        .commit() flush's the commit (whatever is in add.()) and actually runs the submission to the database.
    '''

# adding means to get it the db ready
    db.add(todo_model)
# means to flush the pending changes and commit the current items to the DB
    db.commit()


@router.put('/todo/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(db:db_dependency,todo_request:TodoRequest, todo_id: int = Path(gt =0)):
    # todo_model is the todo that we find in the db that matches the todo we want to update
    todo_model= db.query(Todos).filter(Todos.id == todo_id).first()
    # if we can't find the todo - then return to the user none exists!
    if todo_model is None: 
        raise HTTPException(status_code=404, detail="Todo not found")

    # update all of the attributes
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.priority = todo_request.priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@router.delete('/todos/{todo_id}', status_code=status.HTTP_204_NO_CONTENT)

async def delete_todo(db:db_dependency, todo_id: int = Path(gt=0)):
    # query the DB and gather all of the Todos and filter by ID
    # once we find the matching Todo
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

    # if we cant find a matching id then raise an exception
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # otherwise since we found our Todo delete it
    # filter and find the todo, delete it and then commit it as a transcation to our DB
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
