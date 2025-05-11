const express = require("express");
const dotenv = require("dotenv");
const cors = require("cors");
const connectDB = require("./config/db");
const eventRoutes = require("./routes/eventRoutes");
const { initializeEvents } = require("./controllers/eventController");
const promBundle = require("express-prom-bundle");
const metricsMiddleware = promBundle({ includeMethod: true });


// .env
dotenv.config();

connectDB();

const app = express();
app.use(metricsMiddleware);

app.use(cors());
app.use(express.json());

app.use("/api/events", eventRoutes);

initializeEvents();

const PORT = process.env.PORT || 5000;
app.listen(PORT, '0.0.0.0', () => console.log(`🚀 Event Service running on port ${PORT}`));
