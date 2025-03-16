from app import db

class TicketBooking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False) 
    event_id = db.Column(db.String(50), nullable=False)  
    tickets = db.Column(db.Integer, nullable=False)  
    payment_status = db.Column(db.String(50), default='Pending')  

    def __repr__(self):
        return f'<TicketBooking User: {self.user_id} | Event: {self.event_id} | Tickets: {self.tickets}>'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    booking_id = db.Column(db.Integer, db.ForeignKey('ticket_booking.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending') 

    booking = db.relationship('TicketBooking', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return f'<Payment Booking ID: {self.booking_id} | Amount: {self.amount} | Status: {self.status}>'
