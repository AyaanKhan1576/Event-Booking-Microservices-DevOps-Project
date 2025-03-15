# Use the specified minimal base image
FROM python:3.13.1-slim

# Set the working directory to the current directory of user-service
WORKDIR /app

# Copy all files into the container (files/folders listed in .dockerignore will be excluded)
COPY . .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port on which the app will run
EXPOSE 8000

# Startup command to run the FastAPI application using uvicorn
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

