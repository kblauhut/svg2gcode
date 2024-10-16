# Use the official Python image from the Docker Hub
FROM --platform=linux/amd64 python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install required packages
RUN apt-get update && apt-get install -y \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and extract the Juicy G-code binary
RUN wget -q https://github.com/domoszlai/juicy-gcode/releases/download/v1.0.0.0/juicy-gcode-1.0.0.0-linux64.tar.gz \
    && tar -xzf juicy-gcode-1.0.0.0-linux64.tar.gz \
    && mv juicy-gcode-1.0.0.0/juicy-gcode /app/juicy-gcode \
    && chmod +x /app/juicy-gcode \
    && rm juicy-gcode-1.0.0.0-linux64.tar.gz \
    && rm -rf juicy-gcode-1.0.0.0

# Copy the G-code configuration file into the container
COPY gcodeconfig.yml .

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY app.py .

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["python", "app.py"]
