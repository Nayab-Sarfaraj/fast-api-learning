from fastapi import FastAPI,status,Depends,HTTPException    
from complete_application.schema import User_Create_Request
from sqlalchemy.orm import Session
from complete_application.db import get_db,Base,engine
from complete_application.models import User
from datetime import datetime, timedelta
import uuid
from typing import Any

from jose import jwt
# from passlib.context import CryptContext

# pwd_context = CryptContext(
#     schemes=["bcrypt"],
#     deprecated="auto"
# )

from pwdlib import PasswordHash

password_hasher = PasswordHash.recommended()


app=FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/users",status_code=status.HTTP_201_CREATED)
def create_user(user:User_Create_Request,db:Session=Depends(get_db)):
    user.password=password_hasher.hash(user.password)
    new_user = User(email=user.email,password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}")
def get_user(id:int,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"User with {id} does not exits")

    return user


@app.post("/login")
def login(user:User_Create_Request,db:Session=Depends(get_db)):
    db_user = db.query(User).filter(User.email==user.email).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid credentials")

    isValid=password_hasher.verify(user.password,db_user.password)
    if not isValid:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid credentials")
    data={"user_id":db_user.id}
    to_encode = data.copy()

    SECRET_KEY = "your-secret-key"
    ALGORITHM = "HS256"
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {"token":token}

    

    


@app.get("/")
def index():
    return {"status":status.HTTP_200_OK,"message":"Server is running 💀....."}