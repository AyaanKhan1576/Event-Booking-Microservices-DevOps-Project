const Event = require("../models/eventModel");

// Predefined events
const sampleEvents = [
  {
    name: "Oktoberfest",
    date: new Date("2024-09-21T10:00:00.000Z"),
    location: "Munich, Germany",
    description: "The world's largest beer festival with great music and food.",
    price: 50,
    availableTickets: 5000,
  },
  {
    name: "Coachella",
    date: new Date("2024-04-12T18:00:00.000Z"),
    location: "California, USA",
    description: "A massive annual music and arts festival.",
    price: 400,
    availableTickets: 10000,
  },
  {
    name: "Tomorrowland",
    date: new Date("2024-07-19T12:00:00.000Z"),
    location: "Boom, Belgium",
    description: "The biggest electronic dance music festival.",
    price: 300,
    availableTickets: 15000,
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
    const events = await Event.find();
    res.status(200).json(events);
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Server Error" });
  }
};
