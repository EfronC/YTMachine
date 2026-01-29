# Use an official Python image as a base
FROM python:3.10-slim-bookworm

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# ---------------------------
# System dependencies
# ---------------------------
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    gnupg \
    mpv \
    libmpv-dev \
    pulseaudio \
    ffmpeg \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------
# Install Node.js (LTS)
# ---------------------------
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && npm install -g npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ---------------------------
# Install Deno
# ---------------------------
ENV DENO_VERSION=2.0.0
RUN curl -fsSL https://deno.land/x/install/install.sh | sh -s v${DENO_VERSION}

# Add Deno to PATH
ENV DENO_INSTALL=/root/.deno
ENV PATH=${DENO_INSTALL}/bin:${PATH}

# ---------------------------
# App setup
# ---------------------------
WORKDIR /app

# Copy application code
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 5000

# Command to run the Flask app
CMD ["python", "app.py"]
