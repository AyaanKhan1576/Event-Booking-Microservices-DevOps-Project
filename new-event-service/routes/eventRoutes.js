const express = require("express");
const { getAllEvents, getEventByEventId } = require("../controllers/eventController");

const router = express.Router();

router.get("/", getAllEvents);
router.get("/:eventId", getEventByEventId);

module.exports = router;
