const express = require("express");
const dotenv = require("dotenv");
const cors = require("cors");
const helmet = require("helmet");
const morgan = require("morgan");
const winston = require("winston");
const connectDB = require("./config/db");
const eventRoutes = require("./routes/eventRoutes");
const errorHandler = require("./middleware/errorHandler");

dotenv.config();
connectDB();

const app = express();
const PORT = process.env.PORT || 5000;

// Winston logger setup
const logger = winston.createLogger({
  level: "info",
  format: winston.format.json(),
  transports: [
    new winston.transports.File({ filename: "logs/event-service.log" }),
  ],
});

app.use(helmet());  // Security
app.use(cors());  // Enable CORS
app.use(express.json());  // JSON Parsing
app.use(morgan("combined", { stream: { write: (message) => logger.info(message) } }));

// Routes
app.use("/api/events", eventRoutes);

// Error handling middleware
app.use(errorHandler);

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
