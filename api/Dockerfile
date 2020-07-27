# Use Python image
FROM python:latest

# Set working directory to /app
WORKDIR /app

# Copy the current directory content into the /app folder of the image
ADD . /app

# Install all dependencies
RUN pip install -r requirements.txt

# Run command to start uWSGI
CMD ["uwsgi", "app.ini"]