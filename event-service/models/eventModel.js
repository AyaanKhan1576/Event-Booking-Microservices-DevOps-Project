const mongoose = require("mongoose");

const eventSchema = new mongoose.Schema({
  _id: { type: Number, required: true }, // Change ObjectId to Number
  name: { type: String, required: true },
  date: { type: Date, required: true },
  location: { type: String, required: true },
  description: { type: String, required: true },
  price: { type: Number, required: true },
  availableTickets: { type: Number, required: true },
});

const Event = mongoose.model("Event", eventSchema);

module.exports = Event;
