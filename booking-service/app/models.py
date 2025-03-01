from app import db

class TicketBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_name = db.Column(db.String(120), nullable=False)
    user_name = db.Column(db.String(120), nullable=False)
    payment_status = db.Column(db.String(50), default='Pending')  # Could be 'Pending', 'Paid'

    def __repr__(self):
        return f'<TicketBooking {self.event_name} - {self.user_name}>'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('ticket_booking.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending')

    booking = db.relationship('TicketBooking', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f'<Payment {self.amount} - {self.status}>'
