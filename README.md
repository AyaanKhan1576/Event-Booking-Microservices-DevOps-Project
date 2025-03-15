# CS4067 Event Booking Microservices

## Contributors
- **Ayaan Khan (22i-0832)**
- **Minahil Ali (22i-0849)**

## Overview
This repository contains the code for an Event Booking application built using a microservices architecture. The project is divided into the following services:
- **User Service:** Handles user authentication and profiles.
- **Event Service:** Manages event listings.
- **Booking Service:** Manages ticket bookings, payment processing, and booking status.
- **Notification Service:** Sends out confirmation notifications via email/SMS.

## Repository Structure
- **user-service/**: Code for user authentication and profile management.
- **event-service/**: Code for event listing and management.
- **booking-service/**: Code for processing bookings and integrating with RabbitMQ.
- **notification-service/**: Code for handling notifications.

Event Booking Project  
│   .gitignore             # Specifies files to ignore in Git version control  
│   erl_crash.dump         # Erlang crash dump file (can be ignored or deleted)  
│   help.txt               # Possibly a help file (contents unknown)  
│   package-lock.json      # Dependency lock file for Node.js services  
│   README.md              # Project documentation file  
│   structure.txt          # Contains the project structure (likely this file)  
│  
├── booking-service        # Handles event booking and payment processing  
│   │   .env               # Environment variables for configuration  
│   │   .gitignore         # Git ignore file for booking service  
│   │   booking-service.log # Log file for debugging  
│   │   create_db.py       # Script to create and initialize the database  
│   │   erl_crash.dump     # Erlang crash log (possibly from RabbitMQ)  
│   │   README.md          # Documentation for the booking service  
│   │   requirements.txt   # Python dependencies for this service  
│   │   run.py             # Main entry point for the booking service  
│   │  
│   ├── app                # Core application logic  
│   │   │   config.py      # Configuration settings  
│   │   │   models.py      # Database models (tables and schemas)  
│   │   │   tasks.py       # Background tasks (RabbitMQ processing)  
│   │   │   utils.py       # Utility functions  
│   │   │   views.py       # API endpoints for handling booking requests  
│   │   │   __init__.py    # Marks the folder as a Python package  
│   │   ├── __pycache__    # Cached Python files (can be ignored)  
│   │  
│   ├── migrations         # Database migration scripts  
│   │   │   alembic.ini    # Alembic configuration for database migrations  
│   │   │   env.py         # Migration environment settings  
│   │   │   README         # Migration readme file  
│   │   │   script.py.mako # Template for Alembic migrations  
│   │  
│   ├── __pycache__        # Cached Python files  
│  
├── new-event-service      # Manages events data (CRUD operations)  
│   │   .gitignore         # Git ignore file for event service  
│   │   package.json       # Dependencies and scripts for Node.js service  
│   │   server.js          # Main entry point for the event service  
│   │  
│   ├── config  
│   │   │   db.js          # Database connection settings  
│   │  
│   ├── controllers  
│   │   │   eventController.js  # Handles event-related business logic  
│   │  
│   ├── models  
│   │   │   Event.js       # Mongoose schema for events  
│   │  
│   ├── routes  
│       │   eventRoutes.js # Defines API routes for events  
│  
├── notification-service   # Handles sending notifications (RabbitMQ consumer)  
│   │   .env.example       # Example environment file  
│   │   .gitignore         # Git ignore file for notification service  
│   │   package-lock.json  # Dependency lock file  
│   │   package.json       # Node.js dependencies  
│   │   README.md          # Documentation for notification service  
│   │   server.js          # Main entry point for the notification service  
│   │   test-producer.js   # Script to test RabbitMQ message publishing  
│  
├── user-service           # Manages users and authentication (FastAPI)  
│   │   .env               # Environment variables for configuration  
│   │   .env.example       # Example environment file  
│   │   .gitignore         # Git ignore file  
│   │   auth.py            # Handles authentication (login, signup, JWT)  
│   │   database.py        # Database connection logic (PostgreSQL)  
│   │   main.py            # FastAPI app entry point  
│   │   models.py          # User database models  
│   │   README.md          # Documentation for user service  
│   │   requirements.txt   # Python dependencies  
│   │  
│   ├── logs  
│   │   │   user-service.log  # Log file for debugging  
│   │  
│   ├── routes  
│   │   ├── frontend.py    # Handles HTML page rendering for users  
│   │   ├── __pycache__    # Cached Python files  
│   │  
│   ├── static             # Static assets (CSS, images)  
│   │   │   style.css      # Stylesheet for frontend  
│   │  
│   ├── templates          # HTML templates for the frontend  
│   │   │   base.html          # Base template layout  
│   │   │   booking_success.html # Booking confirmation page  
│   │   │   book_ticket.html    # Ticket booking form  
│   │   │   dashboard.html      # User dashboard  
│   │   │   events.html         # Displays available events  
│   │   │   home.html           # Homepage  
│   │   │   login.html          # Login page  
│   │   │   register.html       # Registration page  
│   │  
│   ├── __pycache__        # Cached Python files  



## Architecture

### Microservices and Technologies:
1. **User Service** (FastAPI, PostgreSQL, REST API)  
   - Handles user authentication (registration, login, credential verification).
   - Communicates with the Booking Service and Event Service via REST API.

2. **Event Service** (Node.js, MongoDB, REST API)  
   - Provides event details.
   - Interacts with the Booking Service for event availability.

3. **Booking Service** (Flask, PostgreSQL, REST API, RabbitMQ)  
   - Handles event booking and payment processing.
   - Publishes booking confirmation events asynchronously via RabbitMQ.

4. **Notification Service** (Express.js, MongoDB, RabbitMQ)  
   - Listens for booking confirmation messages via RabbitMQ.
   - Sends notifications to users.

### Communication Flow:
- **User Service** interacts with **Booking Service** and **Event Service** via REST API.
- **Booking Service** processes payments and publishes booking confirmations via **RabbitMQ**.
- **Notification Service** listens for booking events in **RabbitMQ** and sends notifications.

## API Documentation

### User Service (REST API)
#### Authentication Endpoints
- **POST /register** – Create a new user account.
- **POST /login** – Authenticate a user and return a token.
- **GET /users/{user_id}** – Retrieve user details.
- **GET /events - Retrieve evevbt details

### Event Service (REST API)
#### Event Endpoints
- **GET /events** – Retrieve all events.
- **GET /events/{event_id}** – Retrieve a specific event.

### Booking Service (RabbitMQ and REST API)
#### Booking Endpoints
- **POST /book** – Book an event and process payment.
- **GET /bookings/{user_id}** – Retrieve user’s booking history.

### Notification Service (REST API)
#### Notification Endpoints
- **GET /notifications/{user_id}** – Retrieve user notifications.

## Setup Guide

### 1. Clone the Repository
```sh
$ git clone <repo-url>
$ cd event-booking-system
```

### 2. Setup Environment Variables
Create a `.env` file in each microservice directory with the following variables:

#### User Service (`.env`)
```
DATABASE_URL=postgresql://user:password@localhost/userdb
SECRET_KEY=your_secret_key
```

#### Notification Service (`.env`)
```
MONGO_URI=mongodb://localhost:27017/notifications
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
```

### 3. Run Services
#### Start PostgreSQL & MongoDB
Ensure PostgreSQL and MongoDB are running before starting the services.

#### Start RabbitMQ

#### Run User Service
```sh
cd user-service
pip install -r requirements.txt
uvicorn main:app --reload
```

#### Run Event Service
```sh
cd event-service
npm install
node server.js
```

#### Run Booking Service
```sh
cd booking-service
pip install -r requirements.txt
python create_db.py
python run.py
```

#### Run Notification Service
```sh
cd notification-service
npm install
node server.js
```

## Git Workflow
```sh
git checkout -b feature-branch
# Make changes
git add .
git commit -m "Added new feature"
git push origin feature-branch
```


## License
This project is licensed under the MIT License.


