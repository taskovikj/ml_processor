# Use the official Python base image
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install project dependencies
RUN pip install --no-cache-dir Flask gunicorn celery[redis]

# Command to run your Python application
CMD [ "gunicorn", "app:app", "-b", "0.0.0.0:8001" ]
