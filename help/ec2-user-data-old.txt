#!/bin/bash
yum update -y
amazon-linux-extras install docker -y
service docker start
usermod -a -G docker ec2-user

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Clone your GitHub repo
cd /home/ec2-user
git clone https://github.com/AyaanKhan1576/Event-Booking-Microservices-DevOps-Project.git
cd Event-Booking-Microservices-DevOps-Project

# Give ec2-user ownership of the files
chown -R ec2-user:ec2-user /home/ec2-user/Event-Booking-Microservices-DevOps-Project

# (Optional) Wait for Docker socket
sleep 10

# Start app (make sure docker-compose.yml is in repo root)
sudo -u ec2-user docker-compose up -d --build
