# Use Python 3.13 slim image based on Debian Bookworm
FROM python:3.12-slim-bookworm

# Prevent Python from buffering stdout/stderr and creating .pyc files
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory inside the container
WORKDIR /app

# Install system dependencies required for Wagtail, Django, and image handling
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libwebp-dev \
    libffi-dev \
    libssl-dev \
    gettext \
 && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make sure the entrypoint script is executable
RUN chmod +x entrypoint.sh

# Expose the default port for Django dev server
EXPOSE 8000

# Default command to run when container starts
CMD ["./entrypoint.sh"]
