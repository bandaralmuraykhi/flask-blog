# Use an official Python runtime as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code to the container
COPY . .

# Expose a port for the Flask application to listen on
EXPOSE 5005

# Define the command to run when the container starts
CMD ["python", "flask --app flaskr run --debug --port 5004"]
