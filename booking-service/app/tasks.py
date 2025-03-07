import requests
from app import db
from app.models import TicketBooking, Payment
from celery import shared_task

PAYMENT_GATEWAY_URL = "http://localhost:5001/payments"  # Mock Payment Service URL

@shared_task
def process_payment(booking_id):
    """Handles payment processing asynchronously"""
    booking = TicketBooking.query.get(booking_id)
    if not booking:
        return {"error": "Booking not found"}

    amount = booking.tickets * 10  # Example: $10 per ticket
    payment_payload = {"user_id": booking.user_id, "amount": amount}

    try:
        response = requests.post(PAYMENT_GATEWAY_URL, json=payment_payload)
        if response.status_code == 200:
            booking.payment_status = "Paid"
        else:
            booking.payment_status = "Failed"

        db.session.commit()
        return {"message": "Payment processed", "booking_id": booking.id, "status": booking.payment_status}
    
    except Exception as e:
        booking.payment_status = "Failed"
        db.session.commit()
        return {"error": "Payment processing failed", "details": str(e)}
