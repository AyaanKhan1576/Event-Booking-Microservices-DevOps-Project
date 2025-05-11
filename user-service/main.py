from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from fastapi.middleware.cors import CORSMiddleware
import requests
import logging
import os
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from database import SessionLocal, engine
from models import Base, User
from auth import hash_password, authenticate_user



# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # prints to console
        logging.FileHandler("logs/user-service.log"),  # saves to file
    ]
)
logger = logging.getLogger("my_app_logger")

app = FastAPI()
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

# Add session middleware for authentication
app.add_middleware(SessionMiddleware, secret_key="123456789")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
templates = Jinja2Templates(directory="templates")

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
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login/")
def login_user(
    request: Request, 
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, email, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    
    request.session["user_id"] = user.id
    request.session["email"] = user.email
    
    return RedirectResponse(url="/home", status_code=303)

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register/")
def register_user(
    request: Request, 
    name: str = Form(...), 
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
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
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)

# ------------------------------
# PROTECTED ROUTES
# ------------------------------

def get_current_user(request: Request):
    if "user_id" not in request.session:
        return None
    return request.session["email"]

@app.get("/home")
def home_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("home.html", {"request": request, "user": user})

# ------------------------------
# RAW EVENTS ENDPOINT FOR DEBUGGING
# ------------------------------

@app.get("/raw-events")
def raw_events_page(request: Request):
    try:
        response = requests.get("http://127.0.0.1:5000/api/events", timeout=100)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        logger.error("Error fetching raw events: %s", e)
        return {"error": "Failed to fetch raw events."}

# ------------------------------
# EVENTS PAGE
# ------------------------------
EVENT_SERVICE_URL = os.getenv("EVENT_SERVICE_URL", "http://new-event-service:5000/api/events")
# EVENT_SERVICE_URL = "http://localhost:5000/api/events"

@app.get("/events")
def events_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=303)
    
    try:
        response = requests.get(EVENT_SERVICE_URL, timeout=100)
        response.raise_for_status()
        events = response.json()
    except Exception as e:
        logger.error("Error fetching events: %s", e)
        events = []

    return templates.TemplateResponse("events.html", {"request": request, "user": user, "events": events})


# ------------------------------
# BOOKING PAGE
# ------------------------------

@app.get("/book")
def book_ticket_page(request: Request):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse("book_ticket.html", {"request": request, "user": user})

#BOOKING_SERVICE_URL = "http://localhost:5001/book_ticket"  # Change to actual URL
BOOKING_SERVICE_URL = os.getenv("BOOKING_SERVICE_URL", "http://booking-service:5001/book_ticket")
@app.post("/book")
def book_ticket(
    request: Request,
    event_id: int = Form(...),
    tickets: int = Form(...),
):
    user = get_current_user(request)
    if not user:
        return RedirectResponse(url="/", status_code=303)

    booking_data = {
        "user_id": request.session["user_id"],  
        "event_id": event_id,
        "tickets": tickets
    }

    try:
        response = requests.post(BOOKING_SERVICE_URL, json=booking_data, timeout=10)
        response.raise_for_status()

        # Check if there is an issue with ticket availability
        if response.status_code == 400 and "Not enough tickets available" in response.text:
            return templates.TemplateResponse(
                "book_ticket.html",
                {"request": request, "user": user, "error": "Not enough tickets available for this event."}
            )

        # Successful booking
        if response.status_code == 201:
            booking_id = response.json().get("booking_id")  
            message = "Booking successful!"

            # Redirect to the booking_successful.html page
            return templates.TemplateResponse(
                "booking_success.html",
                {"request": request, "user": user, "message": message, "booking_id": booking_id}
            )

        # General booking failure
        else:
            return templates.TemplateResponse(
                "book_ticket.html",
                {"request": request, "user": user, "error": "Booking failed."}
            )
    except requests.exceptions.RequestException as e:
        logger.error(f"Error booking ticket: {e}")
        return templates.TemplateResponse(
            "book_ticket.html",
            {"request": request, "user": user, "error": "Service unavailable."}
        )

@app.on_event("startup")
async def _startup():
    Instrumentator().instrument(app).expose(app)
