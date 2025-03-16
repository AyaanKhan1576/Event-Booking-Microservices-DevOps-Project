require("dotenv").config();
const express = require("express");
const mongoose = require("mongoose");
const amqp = require("amqplib");

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 5000;
const MONGO_URI = process.env.MONGO_URI;
const RABBITMQ_URL = process.env.RABBITMQ_URL;

const notificationSchema = new mongoose.Schema({
  userId: String,
  message: String,
  timestamp: { type: Date, default: Date.now }
});
const Notification = mongoose.model("Notification", notificationSchema);

mongoose.connect(MONGO_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log("✅ Connected to MongoDB"))
  .catch(err => console.error("❌ MongoDB Connection Error:", err));

async function consumeMessages() {
  try {
    const connection = await amqp.connect(RABBITMQ_URL);
    const channel = await connection.createChannel();
    await channel.assertQueue("notifications");

    console.log("📥 Waiting for messages in the 'notifications' queue...");
    channel.consume("notifications", async (msg) => {
      if (msg) {
        const notification = JSON.parse(msg.content.toString());
        console.log("🔔 Received Notification:", notification);

        await Notification.create(notification);
        console.log("✅ Notification saved to DB");

        channel.ack(msg);
      }
    });
  } catch (error) {
    console.error("❌ RabbitMQ Connection Error:", error);
  }
}

consumeMessages();

// API Endpoint to Get Notifications
app.get("/notifications", async (req, res) => {
  const notifications = await Notification.find();
  res.json(notifications);
});

app.listen(PORT, () => console.log(`🚀 Notification Service running on port ${PORT}`));
