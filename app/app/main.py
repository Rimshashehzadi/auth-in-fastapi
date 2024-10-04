from fastapi import FastAPI, HTTPException, Depends
from sqlmodel import Session , select
# from sqlmodel import select
from .models import User, engine
from .schemas import UserCreate
from .email_services import send_otp # type: ignore
# from models import User, engine
# from schemas import UserCreate
# from email_service import send_otp # type: ignore

app = FastAPI()

def get_db():
    with Session(engine) as session:
        yield session

@app.post("/signup/")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Check if the user already exists
    existing_user = db.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create the new user
    new_user = User(email=user.email, hashed_password=user.password)  # Hash the password in a real application
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Send OTP
    otp = send_otp(user.email)
    new_user.otp = otp
    db.add(new_user)
    db.commit()

    return {"message": "User created successfully, OTP sent to your email."}

# Run the application with the command:
# uvicorn main:app --reload
