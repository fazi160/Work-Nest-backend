
# Use the official Python image with the specified version
FROM python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install system dependencies for Twisted
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        libffi-dev \
        openssl

# Set the working directory
WORKDIR /app/backend

# Copy the requirements file to the working directory
COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project to the working directory
COPY . .

# Command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

