from app import app, db
import requests
from flask import request, jsonify
from app.models import TicketBooking, Payment
from app.tasks import process_payment  
import os


#EVENT_SERVICE_URL = "http://localhost:5000/api/events"
EVENT_SERVICE_URL = os.getenv("EVENT_SERVICE_URL", "http://new-event-service:5000/api/events")
#PAYMENT_GATEWAY_URL = "http://localhost:5001/payments"  # Mock Payment Service URL
PAYMENT_GATEWAY_URL = os.getenv("PAYMENT_GATEWAY_URL", "http://booking-service:5001/payments")
#http://localhost:5000/api/events/{event_id}/availability

@app.route('/book_ticket', methods=['POST'])
def book_ticket_flask():
    """Handles booking requests from User Service"""
    data = request.json
    user_id = data.get('user_id')
    event_id = data.get('event_id')
    tickets = data.get('tickets')

    if not all([user_id, event_id, tickets]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Step 1: Check event availability from Event Service
        event_url = f"{EVENT_SERVICE_URL}/{event_id}/availability"
        event_response = requests.get(event_url)

        if event_response.status_code != 200:
            return jsonify({"error": "Failed to check event availability"}), 500

        availability = event_response.json()

        if not availability.get("isAvailable") or availability.get("availableTickets") < tickets:
            return jsonify({"error": "Not enough tickets available"}), 400

        # Step 2: Calculate total amount (assuming ticket price is $10 per ticket)
        amount = tickets * 10  

        # Step 3: Call Payment API
        payment_payload = {"user_id": user_id, "amount": amount}
        payment_response = requests.post(PAYMENT_GATEWAY_URL, json=payment_payload)

        if payment_response.status_code == 200:
            payment_status = "Paid"
        else:
            payment_status = "Failed"

        # Step 4: Create a new booking with payment status
        booking = TicketBooking(user_id=user_id, event_id=event_id, tickets=tickets, payment_status=payment_status)
        db.session.add(booking)
        db.session.commit()

        return jsonify({"message": "Booking created successfully!", "booking_id": booking.id, "payment_status": payment_status}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create booking", "details": str(e)}), 500
        
@app.route("/payments", methods=["POST"])
def process_payment():
    data = request.json
    user_id = data.get("user_id")
    amount = data.get("amount")

    if not user_id or not amount:
        return jsonify({"error": "Missing user_id or amount"}), 400

    # Simulate random success/failure
    import random
    success = random.choice([True, False])

    if success:
        return jsonify({"message": "Payment successful", "status": "Paid"}), 200
    else:
        return jsonify({"message": "Payment failed", "status": "Failed"}), 400

@app.route('/payment_status/<int:booking_id>', methods=['GET'])
def payment_status(booking_id):
    booking = TicketBooking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    return jsonify({
        "booking_id": booking.id,
        "user_id": booking.user_id,
        "event_id": booking.event_id,
        "tickets": booking.tickets,
        "payment_status": booking.payment_status
    }), 200


@app.route('/api/bookings', methods=['GET'])
def get_all_bookings():
    """Fetches all bookings from the database."""
    bookings = TicketBooking.query.all()
    bookings_list = [{
        "id": booking.id,
        "user_id": booking.user_id,
        "event_id": booking.event_id,
        "tickets": booking.tickets,
        "payment_status": booking.payment_status
    } for booking in bookings]

    return jsonify(bookings_list), 200
