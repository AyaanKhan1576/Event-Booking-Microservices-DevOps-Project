from app import celery
from app.models import TicketBooking, Payment
from app import db
import time

@celery.task
def process_payment(booking_id):
    # Simulate payment processing time
    time.sleep(5)

    booking = TicketBooking.query.get(booking_id)
    if booking:
        # After payment is processed (for now, we mock it)
        payment = Payment(booking_id=booking.id, amount=100.0, status='Paid')
        db.session.add(payment)
        booking.payment_status = 'Paid'
        db.session.commit()

    return f'Payment processed for booking {booking_id}'
