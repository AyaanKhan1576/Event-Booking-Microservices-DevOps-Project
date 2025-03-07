const mongoose = require("mongoose");

const eventSchema = new mongoose.Schema({
    eventId: { type: Number, required: true, unique: true }, 
    name: { type: String, required: true },
    date: { type: String, required: true },
    location: { type: String, required: true },
    price: { type: Number, required: true },
    availableTickets: { type: Number, required: true },
    bookedTickets: { type: Number, default: 0 }, // ✅ Track booked tickets
    totalTickets: { type: Number, required: true }, // ✅ Total tickets available
});

const Event = mongoose.model("Event", eventSchema);

module.exports = Event;
