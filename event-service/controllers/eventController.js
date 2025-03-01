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
  {
    name: "Glastonbury Festival",
    date: new Date("2024-06-26T09:00:00.000Z"),
    location: "Pilton, UK",
    description: "A five-day festival of contemporary performing arts.",
    price: 250,
    availableTickets: 20000,
  },
  {
    name: "Burning Man",
    date: new Date("2024-08-25T08:00:00.000Z"),
    location: "Black Rock City, Nevada",
    description: "A unique festival focused on community and self-expression.",
    price: 475,
    availableTickets: 7000,
  },
  {
    name: "Lollapalooza",
    date: new Date("2024-08-01T14:00:00.000Z"),
    location: "Chicago, USA",
    description: "A four-day music festival featuring various genres.",
    price: 350,
    availableTickets: 12000,
  },
  {
    name: "Rock in Rio",
    date: new Date("2024-09-13T16:00:00.000Z"),
    location: "Rio de Janeiro, Brazil",
    description: "One of the biggest rock and pop festivals.",
    price: 280,
    availableTickets: 9000,
  },
  {
    name: "Ultra Music Festival",
    date: new Date("2024-03-22T17:00:00.000Z"),
    location: "Miami, USA",
    description: "A massive electronic dance music festival.",
    price: 320,
    availableTickets: 8000,
  },
  {
    name: "Summer Sonic",
    date: new Date("2024-08-17T15:00:00.000Z"),
    location: "Tokyo, Japan",
    description: "A two-day rock festival held in Tokyo and Osaka.",
    price: 180,
    availableTickets: 6000,
  },
  {
    name: "Fuji Rock Festival",
    date: new Date("2024-07-26T13:00:00.000Z"),
    location: "Niigata, Japan",
    description: "Japan's largest outdoor music event.",
    price: 250,
    availableTickets: 5000,
  }
];

// @desc   Seed database with sample events
exports.createEvent = async (req, res) => {
  try {
    await Event.insertMany(sampleEvents);
    res.status(201).json({ message: "Events created successfully", events: sampleEvents });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: "Server Error" });
  }
};

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
