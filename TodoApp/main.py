# our table
from fastapi import FastAPI
from database import engine
from routers import auth, todos,admin,users
import models

app = FastAPI()
# creates everything from our models file, and Db file to create a new DB with Todos and all of the columns that have been layed out
# only runs if our todo.db does not exist
models.Base.metadata.create_all(bind=engine)


# route to check if the app is up and running - known as a health check
@app.get('/healthy')
def health_check():
    return {'status': 'Healthy'}

# to include api endpoints from our auth file and todos 
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)

