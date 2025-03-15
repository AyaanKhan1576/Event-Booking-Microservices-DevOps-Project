# Use a base Python image
FROM python:3.13.1-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the application files into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure entrypoint script is executable
RUN chmod +x entrypoint.sh

# Use the entrypoint script
CMD ["sh", "./entrypoint.sh"]
