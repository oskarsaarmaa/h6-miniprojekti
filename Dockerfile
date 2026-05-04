# Use official Python image
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy the app files and the requirements
COPY app/ /app/
COPY .env /app/.env

# Install necessary libraries
RUN pip install flask requests python-dotenv

# Expose the port Flask runs on
EXPOSE 5000

# Start the application
CMD ["python", "main.py"]
