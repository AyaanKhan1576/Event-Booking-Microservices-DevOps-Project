const mongoose = require("mongoose");

const eventSchema = new mongoose.Schema({
    eventId: { type: String, required: true, unique: true },
    name: { type: String, required: true },
    date: { type: String, required: true },
    location: { type: String, required: true },
    price: { type: Number, required: true }
});

const Event = mongoose.model("Event", eventSchema);

module.exports = Event;
