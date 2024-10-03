from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session
from .database import engine, get_db
from .schemas import UserCreate
from .crud import create_user

app = FastAPI()

# Create the database tables
@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)

@app.post("/signup/")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    db_user = create_user(db, user)
    return {"message": "User created successfully", "user_id": db_user.id}
