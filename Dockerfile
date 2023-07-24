# Dockerfile for ml_processor
FROM python:3.8

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install project dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Command to run your Python application (assuming your Flask app is named "app.py")
CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8001"]
