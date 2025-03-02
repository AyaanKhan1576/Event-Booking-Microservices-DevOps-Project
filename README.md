# CS4067 Event Booking Microservices

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

## Contributors
- **Ayaan Khan**
- **Minahil Ali**

## License
This project is licensed under the MIT License.


