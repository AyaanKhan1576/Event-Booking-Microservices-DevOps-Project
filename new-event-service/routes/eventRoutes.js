const express = require("express");
const eventController = require("../controllers/eventController");

const router = express.Router();

router.get("/", eventController.getAllEvents);
router.get("/:eventId", eventController.getEventByEventId);
router.get("/:event_id/availability", eventController.checkAvailability);

module.exports = router;
