# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Create media directory
RUN mkdir -p /app/media /app/media


# Copy the requirements.txt file first
COPY requirements.txt .

# Copy SSL certificates
COPY ./certs/brvn.work.gd.cer /etc/nginx/certs/
COPY ./certs/brvn.work.gd.key /etc/nginx/certs/


RUN apt-get update && apt-get install -y postfix
RUN apt-get update && apt-get install -y opendkim opendkim-tools

RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory into the container
COPY . .

RUN python manage.py collectstatic --noinput
# Expose the port the app runs on
EXPOSE 8000

# Command to run the application with Gunicorn
CMD ["gunicorn", "ec.wsgi:application", "--bind", "0.0.0.0:8000"]
