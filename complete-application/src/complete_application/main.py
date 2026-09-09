from fastapi import FastAPI,status,Depends
from complete_application.schema import User_Create_Request
from sqlalchemy.orm import Session
from complete_application.db import get_db
from complete_application.models import User

app=FastAPI()


@app.post("/users",status_code=status.HTTP_201_CREATED)
def create_user(user:User_Create_Request,db:Session=Depends(get_db)):
    new_user = User()

@app.get("/")
def index():
    return {"status":status.HTTP_200_OK,"message":"Server is running 💀....."}