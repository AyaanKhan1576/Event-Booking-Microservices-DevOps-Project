const mongoose = require("mongoose");
const Event = require("../models/eventModel");
const { ObjectId } = mongoose.Types; // Import ObjectId

const sampleEvents = [
  {
    _id: 1,
    name: "Tech Conference 2025",
    date: "2025-03-15T10:00:00Z",
    location: "New York Convention Center",
    description: "A conference for tech enthusiasts.",
    price: 50,
    availableTickets: 100,
  },
  {
    _id: 2,
    name: "Music Festival",
    date: "2025-04-20T12:00:00Z",
    location: "Los Angeles Open Grounds",
    description: "A grand music festival featuring top artists.",
    price: 75,
    availableTickets: 200,
  },
  {
    _id: 3,
    name: "Startup Networking Event",
    date: "2025-05-10T18:00:00Z",
    location: "San Francisco Tech Hub",
    description: "Meet investors and startup founders.",
    price: 30,
    availableTickets: 150,
  },
];

// Export sampleEvents separately
module.exports.sampleEvents = sampleEvents;

// Controller functions
exports.createEvent = async (req, res) => {
  try {
    await Event.deleteMany({}); // Clear existing data (Optional)
    const events = await Event.insertMany(sampleEvents);
    res.status(201).json({ message: "Events created", events });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Server Error" });
  }
};

exports.getEvents = async (req, res) => {
  try {
    let events = await Event.find();

    // If no events are in the DB, return sampleEvents
    if (events.length === 0) {
      events = sampleEvents;
    }

    const formattedEvents = events.map((event, index) => ({
      _id: event._id || new ObjectId(),  // Use event._id if available, otherwise use the index as a fallback
      name: event.name,
      date: new Date(event.date).toISOString().split("T")[0],
      location: event.location,
      description: event.description,
      price: event.price,
      availableTickets: event.availableTickets,
    }));
    


    res.status(200).json(formattedEvents);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Server Error" });
  }
};
