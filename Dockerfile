# Use the correct Python base image
FROM python:3.9

# Set working directory in container
WORKDIR /app

# Copy contents to the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose default port (Render sets $PORT automatically)
EXPOSE 10000

# Run the app with gunicorn (Render sets $PORT as an env variable)
CMD ["sh", "-c", "gunicorn --workers=4 --bind=0.0.0.0:$PORT app:app"]
