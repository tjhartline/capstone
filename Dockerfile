# Use the official Python image from the Docker Hub
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the local code to the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the port app runs on
EXPOSE $PORT

# Command to run application
CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "csDashboard:app.server"]
