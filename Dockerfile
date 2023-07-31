# Base image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/


RUN python manage.py makemigrations
RUN python manage.py migrate
# Collect static files
RUN python manage.py collectstatic --noinput


# Run Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "myproject.wsgi"]

