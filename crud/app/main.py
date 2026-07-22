from fastapi import Depends, FastAPI,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select


from app.db.database import Base, engine, get_db
from app.db.models import Note
from app.schema.note import Create_Note, Note_Response


app=FastAPI()

Base.metadata.create_all(bind=engine)

# notes=[]

# a function that takes a functions and returns a new function is decorator
# here app.get("/") is a decorator
# the below code is equivalent to this
# def root():
    # return {"message": "Hello"}
# root = app.get("/")(root)

@app.get("/")
def root():
    return {"message":"Hello FastAPI"}


@app.post("/notes",response_model=Note_Response)
def create_note(
    note:Create_Note,
     db: Session = Depends(get_db)
):
    db_note = Note(
        title=note.title
    )
    db.add(db_note)
    db.commit()

    db.refresh(db_note)

    return db_note

@app.get("/notes",response_model=list[Note_Response])
def getAllNotes(
    db:Session=Depends(get_db)
):
    stmt = select(Note)
    notes = db.scalars(stmt).all()
    return notes

@app.get("/note/{id}",response_model=Note_Response)
def get_note(id:int, db:Session=Depends(get_db)):
    stmt=select(Note).where(Note.id==id)
    note=db.scalar(stmt)

    if note is None:
        raise HTTPException(404, "Note not found")
    
    return note

@app.put("/note/{id}",response_model=Note_Response)
def update_note(id: int,
    note: Create_Note,
    db: Session = Depends(get_db)):
    stmt=select(Note).where(Note.id==id)
    db_note=db.scalar(stmt)
    
    if db_note is None:
        raise HTTPException(404,"Note not found")
    
    db_note.title=note.title
    
    db.commit()
    db.refresh(db_note)
    
    return db_note

@app.delete("/note/{id}")
def delete_note(id:int,    db: Session = Depends(get_db)
):
    stmt=select(Note).where(Note.id==id)
    db_note=db.scalar(stmt)

    if db_note is None:
        raise HTTPException(404, "Note not found")


    db.delete(db_note)
    db.commit()
   
    return {
        "message": "Deleted successfully"
    }


# @app.get("/about")
# def about(name:str):
#     return {"message": f"Hello {name}"}

# @app.get("/about/{id}")
# def about(id:int):
#     return {"id":id}


# @app.post("/notes",response_model=Note_Response)
# def create_note(note:Note):
#     print(type(note))
#     print(note.title)
#     print(note.description)
#     print(note.priority)
    # under the hood this is happening
    # notes = [
    #     NoteCreate(
    #         title="Learn FastAPI",
    #         content="Awesome",
    #         priority=1
    #     )
    # ]

    # response={
    #     "id":len(notes)+1,
    #     "title": note.title,
    #     "description": note.description,
    #     "priority": note.priority
    # }

    # notes.append(response)

    # print(type(notes[0]))
    # # output <class 'app.schema.note.Note'> 

    # return response




# What Uvicorn roughly does internally
# When you run:
# uvicorn app.main:app --reload
# Think of it like this:

# import app.main
# application = app.main.app
# start_http_server(application)