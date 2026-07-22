from pydantic import BaseModel

class Create_Note(BaseModel):
    title:str
    # description:str
    # priority:int

class Note_Response(BaseModel):
    id:int
    title:str
    # description:str
    model_config = {
        "from_attributes": True
    }

    # New thing: from_attributes

    # This replaces the old orm_mode = True from Pydantic v1.

    # It tells Pydantic:

    # "You'll receive a SQLAlchemy object, not a dictionary. Read values from its attributes."