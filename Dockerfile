# Use the official Python 3.10 image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt .

# Install system packages (if packages.txt exists)
# COPY packages.txt .
# RUN if [ -f packages.txt ]; then apt-get update && apt-get install -y $(cat packages.txt) && rm packages.txt; fi

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir streamlit

# Copy the rest of the application code
COPY . .

# Expose the port for Streamlit
EXPOSE 3000

# Run the Streamlit app
CMD ["streamlit", "run", "./app/app.py", "--server.enableCORS=false", "--server.enableXsrfProtection=false", "--server.port=3000", "--server.address=0.0.0.0"]