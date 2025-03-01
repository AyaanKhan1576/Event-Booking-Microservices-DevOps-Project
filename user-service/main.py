from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User
from auth import hash_password, authenticate_user
import requests

app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/")
def register_user(email: str, password: str, db: Session = Depends(get_db)):
    hashed_password = hash_password(password)
    new_user = User(email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@app.post("/login/")
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful"}

@app.get("/verify/{email}")
def verify_user(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User verified"}
