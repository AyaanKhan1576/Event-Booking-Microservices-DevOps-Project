const Event = require("../models/Event");

// Populate the database with some events if empty
const initializeEvents = async () => {
    const eventsExist = await Event.countDocuments();
    if (eventsExist === 0) {
        const sampleEvents = [
            {
                eventId: 1,
                name: "Tech Conference 2025",
                date: "2025-06-12",
                location: "New York",
                price: 100,
                availableTickets: 500,  
                totalTickets: 500,  
                bookedTickets: 0  
            },
            {
                eventId: 2,
                name: "Music Festival",
                date: "2025-07-20",
                location: "Los Angeles",
                price: 80,
                availableTickets: 1000,
                totalTickets: 1000,
                bookedTickets: 0
            },
            {
                eventId: 3,
                name: "Art Exhibition",
                date: "2025-09-05",
                location: "San Francisco",
                price: 50,
                availableTickets: 300,
                totalTickets: 300,
                bookedTickets: 0
            }
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
        const eventId = Number(req.params.eventId);
        const event = await Event.findOne({ eventId });

        if (!event) return res.status(404).json({ message: "Event not found" });

        res.json(event);
    } catch (error) {
        res.status(500).json({ message: "Error retrieving event" });
    }
};

// Check availability of an event
const checkAvailability = async (req, res) => {
    const eventId = Number(req.params.event_id); 

    try {
        const event = await Event.findOne({ eventId });
        if (!event) {
            return res.status(404).json({ message: "Event not found" });
        }

        const availableTickets = event.totalTickets - event.bookedTickets;

        res.json({ 
            event_id: eventId, 
            availableTickets, 
            isAvailable: availableTickets > 0 
        });

    } catch (error) {
        console.error("Error checking availability:", error);
        res.status(500).json({ message: "Internal server error" });
    }
};



module.exports = { 
    initializeEvents, 
    getAllEvents, 
    getEventByEventId, 
    checkAvailability
};
