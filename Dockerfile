# Use an official Python runtime as a parent image
FROM python:3.10.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install necessary build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /home
COPY . /app

# Create a user and switch to it (Optional for security)
# RUN adduser --disabled-password --gecos "" myuser
# USER myuser

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "6002"]

# Expose port 8000 (Optional for documentation)
EXPOSE 6002
