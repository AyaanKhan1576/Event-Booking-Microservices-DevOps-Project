# Use the specified Node.js base image
FROM node:22.14.0-alpine

# Set the working directory to the current directory of the new-event-service
WORKDIR /app

# Copy all files into the container (files/folders listed in .dockerignore will be excluded)
COPY . .

# Install dependencies using npm
RUN npm install

# Expose the port on which the service will run
EXPOSE 5000

# Startup command to run the service
CMD ["node", "server.js"]
