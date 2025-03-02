const express = require("express");
const { getEvents } = require("../controllers/eventController");
const router = express.Router();

// Use the formatted getEvents function
router.get("/", getEvents);

// Get event by ID route can remain as is if it matches your needs
router.get("/:id", async (req, res) => {
  try {
    const eventId = parseInt(req.params.id);
    const event = await Event.findOne({ _id: eventId });
    if (!event) {
      return res.status(404).json({ error: "Event not found" });
    }
    res.json(event);
  } catch (error) {
    res.status(500).json({ error: "Failed to fetch event" });
  }
});

module.exports = router;
