# Use a base image
FROM ubuntu:20.04

FROM python:3.9-slim

# Set the working directory in the container to /app
WORKDIR /app

# Create a new file using the 'touch' command
RUN mkdir -p /instance && touch /instance/flaskr.sqlite

# Copy the current directory contents into the container at /app
COPY . /app
COPY flaskr/schema.sql /app/flaskr

# Install the required packages using pip
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5004 available to the world outside this container
EXPOSE 5004

# Define environment variable for Flask to run in production mode
ENV FLASK_APP=flaskr
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Run Flask when the container launches
CMD ["flask", "run", "--port=5002"]
