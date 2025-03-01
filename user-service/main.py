from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from database import SessionLocal, engine
from models import Base, User
from auth import hash_password, authenticate_user
import requests

# Initialize FastAPI App
app = FastAPI()

# Add session middleware for authentication
app.add_middleware(SessionMiddleware, secret_key="123456789")

# Initialize database
Base.metadata.create_all(bind=engine)

# Jinja2 Templates
templates = Jinja2Templates(directory="templates")

# Dependency to get DB Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------------------
# AUTH ROUTES
# ------------------------------

@app.get("/")
def login_page(request: Request):
    """Login Page (First Page)"""
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login/")
def login_user(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Authenticate User"""
    user = authenticate_user(db, email, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    # Store session data
    request.session["user_id"] = user.id
    request.session["email"] = user.email
    
    return RedirectResponse(url="/home", status_code=303)

@app.get("/register")
def register_page(request: Request):
    """Registration Page"""
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register/")
def register_user(
    request: Request, 
    name: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    """Register New User"""
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email already exists"})
    
    hashed_pw = hash_password(password)
    new_user = User(name=name, email=email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    
    return RedirectResponse(url="/", status_code=303)


@app.get("/logout/")
def logout_user(request: Request):
    """Logout User"""
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

# ------------------------------
# PROTECTED ROUTES
# ------------------------------

def get_current_user(request: Request):
    """Get logged-in user"""
    if "user_id" not in request.session:
        return None
    return request.session["email"]

@app.get("/home")
def home_page(request: Request):
    """Home Page - Requires Login"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=303)
    return templates.TemplateResponse("home.html", {"request": request, "user": user})

@app.get("/events")
def events_page(request: Request):
    """Events Page - Requires Login"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=303)
    
    # Fetch events from Event Service
    response = requests.get("http://localhost:8001/events")  # Assuming Event Service runs on 8001
    events = response.json() if response.status_code == 200 else []
    
    return templates.TemplateResponse("events.html", {"request": request, "user": user, "events": events})

@app.get("/book")
def book_ticket_page(request: Request):
    """Book Ticket Page - Requires Login"""
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("book_ticket.html", {"request": request, "user": user})
