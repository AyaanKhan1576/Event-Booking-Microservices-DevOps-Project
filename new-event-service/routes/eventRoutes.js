const express = require("express");
const eventController = require("../controllers/eventController");

const router = express.Router();

// Define routes correctly
router.get("/", eventController.getAllEvents);
router.get("/:eventId", eventController.getEventByEventId);
router.get("/:event_id/availability", eventController.checkAvailability);

// Export the router correctly
module.exports = router;
