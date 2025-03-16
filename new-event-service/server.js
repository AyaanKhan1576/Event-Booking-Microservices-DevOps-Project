const express = require("express");
const dotenv = require("dotenv");
const cors = require("cors");
const connectDB = require("./config/db");
const eventRoutes = require("./routes/eventRoutes");
const { initializeEvents } = require("./controllers/eventController");

dotenv.config();

connectDB();

const app = express();

app.use(cors());
app.use(express.json());

app.use("/api/events", eventRoutes);

initializeEvents();

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`🚀 Event Service running on port ${PORT}`));
