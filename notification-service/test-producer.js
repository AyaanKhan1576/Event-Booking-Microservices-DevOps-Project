const amqp = require('amqplib');

async function sendTestMessage() {
    const connection = await amqp.connect('amqp://localhost');
    const channel = await connection.createChannel();
    const queue = 'notifications';

    const message = JSON.stringify({
        userEmail: "test@example.com",
        message: "Your event has been successfully booked!"
    });

    await channel.assertQueue(queue, { durable: true });
    channel.sendToQueue(queue, Buffer.from(message), { persistent: true });

    console.log("✅ Test message sent:", message);
    setTimeout(() => {
        connection.close();
        process.exit(0);
    }, 500);
}

sendTestMessage().catch(console.error);
