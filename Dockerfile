# Use Python 3.13 as the base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy the entire project
COPY . /app/

# Install the package and its dependencies
RUN pip install --no-cache-dir -e .

# Create a volume for output logs
VOLUME /app/logs

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
ENTRYPOINT ["python", "-m", "random_log_generator.cli"]

# Default arguments (can be overridden at runtime)
CMD ["--config", "config.yaml"]