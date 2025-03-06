const Event = require("../models/Event");
const { v4: uuidv4 } = require("uuid");

// Populate the database with some events if empty
const initializeEvents = async () => {
    const eventsExist = await Event.countDocuments();
    if (eventsExist === 0) {
        const sampleEvents = [
            { eventId: uuidv4(), name: "Tech Conference 2025", date: "2025-06-12", location: "New York", price: 100 },
            { eventId: uuidv4(), name: "Music Festival", date: "2025-07-20", location: "Los Angeles", price: 80 },
            { eventId: uuidv4(), name: "Art Exhibition", date: "2025-09-05", location: "San Francisco", price: 50 }
        ];
        await Event.insertMany(sampleEvents);
        console.log("📌 Sample Events Inserted");
    }
};

// Get all events
const getAllEvents = async (req, res) => {
    try {
        const events = await Event.find();
        res.json(events);
    } catch (error) {
        res.status(500).json({ message: "❌ Error fetching events" });
    }
};

// Get single event by eventId
const getEventByEventId = async (req, res) => {
    try {
        const event = await Event.findOne({ eventId: req.params.eventId });
        if (!event) return res.status(404).json({ message: "Event not found" });
        res.json(event);
    } catch (error) {
        res.status(500).json({ message: " Error retrieving event" });
    }
};

module.exports = { initializeEvents, getAllEvents, getEventByEventId };
