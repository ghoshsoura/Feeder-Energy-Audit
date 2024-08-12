# Dockerfile for Django

# Use an official Python runtime as a parent image
FROM python:3.12.2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /projects

# Install dependencies
COPY requirements.txt /projects/
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /projects/

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "projects.wsgi:application"]
