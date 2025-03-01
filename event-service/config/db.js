const mongoose = require("mongoose");
require("dotenv").config();
const Event = require("../models/eventModel");

// Sample events
const sampleEvents = [ /* same predefined events from before */ ];

const connectDB = async () => {
  try {
    await mongoose.connect(process.env.MONGO_URI);

    console.log("MongoDB connected successfully");

    // Check if database is empty before inserting sample events
    const existingEvents = await Event.countDocuments();
    if (existingEvents === 0) {
      await Event.insertMany(sampleEvents);
      console.log("Sample events added to database.");
    }
  } catch (err) {
    console.error("MongoDB connection error:", err);
    process.exit(1);
  }
};

module.exports = connectDB;
