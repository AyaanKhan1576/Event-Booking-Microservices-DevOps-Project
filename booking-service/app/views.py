from app import app, db
from flask import request, jsonify
from app.models import TicketBooking, Payment
from app.tasks import process_payment  # Async task for RabbitMQ

@app.route('/book_ticket', methods=['POST'])
def book_ticket():
    data = request.json
    event_name = data.get('event_name')
    user_name = data.get('user_name')

    # Create a new booking
    booking = TicketBooking(event_name=event_name, user_name=user_name)
    db.session.add(booking)
    db.session.commit()

    # Initiate payment process
    process_payment.apply_async(args=[booking.id])

    return jsonify({'message': 'Booking created successfully!', 'booking_id': booking.id}), 201

@app.route('/payment_status/<int:booking_id>', methods=['GET'])
def payment_status(booking_id):
    booking = TicketBooking.query.get(booking_id)
    if not booking:
        return jsonify({'error': 'Booking not found'}), 404

    return jsonify({'payment_status': booking.payment_status}), 200
