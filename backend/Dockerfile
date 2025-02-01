# Setting up the Python environment
FROM python:3.9-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Working directory Set
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Container port 8000 open
EXPOSE 8000

# Run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
