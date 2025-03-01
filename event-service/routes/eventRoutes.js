const express = require("express");
const router = express.Router();
const { getEvents, createEvent } = require("../controllers/eventController");

router.get("/", getEvents);
router.post("/seed", createEvent); // New route to populate database

module.exports = router;
