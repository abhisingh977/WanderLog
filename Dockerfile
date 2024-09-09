# Use an official Python runtime as the base image
FROM python:3.9-slim
# Set environment variables
ENV PIP_NO_CACHE_DIR=false
ENV PIP_PROGRESS_BAR=off

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Install the required packages
# RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--log-level", "info", "main:app"]
