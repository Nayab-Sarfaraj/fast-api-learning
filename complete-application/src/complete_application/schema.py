from pydantic import BaseModel,EmailStr

class User_Create_Request(BaseModel):
    email:EmailStr
    password:str