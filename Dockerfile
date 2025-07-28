# Use a base image that includes Python
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire current directory contents into the container
COPY . .

# Set the command to run your application
CMD ["python", "main.py"]

# Expose the port that the app runs on (if necessary)
EXPOSE 8000
