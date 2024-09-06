# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN cat requirements.txt | xargs -n 1 pip install
# Install the required packages
# RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "main:app"]