# Use an official Python image as a base
FROM python:3.10-slim

# Install dependencies for MPV
RUN apt-get update && apt-get install -y \
    mpv \
    libmpv-dev \
    pulseaudio \
    ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy application code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]