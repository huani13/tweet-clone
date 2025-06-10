# Dockerfile

# --- Stage 1: Build Stage ---
# Use an official Python image as a parent image
FROM python:3.11-slim as builder

# Set the working directory in the container
WORKDIR /app

# Install build dependencies if any (e.g., for packages that compile from source)
# RUN apt-get update && apt-get install -y build-essential

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# --- Stage 2: Final Stage ---
# Use a smaller, clean base image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the pre-built wheels from the builder stage
COPY --from=builder /app/wheels /wheels

# Install the dependencies from the local wheels
RUN pip install --no-cache /wheels/*

# Copy your application code into the container
COPY . .

# Expose the port the app runs on
EXPOSE 8000

# The command to run the application
# This is the most important line for production
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]