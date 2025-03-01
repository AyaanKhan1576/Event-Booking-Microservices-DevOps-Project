from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, User
from auth import hash_password, authenticate_user
from routes import frontend
import uvicorn

app = FastAPI()
Base.metadata.create_all(bind=engine)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Include frontend routes
app.include_router(frontend.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/")
def register_user(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    hashed_password = hash_password(password)
    new_user = User(email=email, password=hashed_password)
    db.add(new_user)
    db.commit()
    return templates.TemplateResponse("register.html", {"request": request, "message": "User registered successfully"})

@app.post("/login/")
def login_user(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return templates.TemplateResponse("dashboard.html", {"request": request, "email": email})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
