const express = require("express");
const router = express.Router();
const { getEvents, createEvent } = require("../controllers/eventController");

router.get("/", getEvents);
router.post("/", createEvent);

module.exports = router;
