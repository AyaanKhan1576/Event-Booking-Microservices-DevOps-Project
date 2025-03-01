const Event = require("../models/eventModel");

// @desc   Get all events
exports.getEvents = async (req, res) => {
  try {
    const events = await Event.find();
    res.status(200).json(events);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Server Error" });
  }
};

// @desc   Create a new event
exports.createEvent = async (req, res) => {
    try {
      const { name, date, location, description, price, availableTickets } = req.body;
  
      if (!name || !date || !location || price === undefined || availableTickets === undefined) {
        return res.status(400).json({ message: "Missing required fields" });
      }
  
      const event = new Event({ name, date, location, description, price, availableTickets });
      await event.save();
  
      res.status(201).json({ message: "Event created successfully", event });
    } catch (error) {
      console.error(error);
      res.status(500).json({ message: "Server Error" });
    }
  };
  
