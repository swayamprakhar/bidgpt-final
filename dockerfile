FROM python:3.11-slim

WORKDIR /app

COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the port for Fly.io
ENV PORT 8080

# Expose the port
EXPOSE 8080

# Start the Flask app
CMD ["python", "server.py"]
