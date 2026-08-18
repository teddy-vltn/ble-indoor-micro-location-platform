# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_NO_CACHE_DIR=1 \
    PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install dependencies
COPY ./modules/graph-positioning/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install Ansible and tzdata for timezone settings
RUN apt-get update && \
    apt-get install -y tzdata && \
    apt-get clean

# Set the timezone to Europe/Paris
RUN ln -fs /usr/share/zoneinfo/Europe/Paris /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

COPY ./modules ./modules
COPY ./config.yaml ./config.yaml

CMD ["python", "./modules/graph-positioning/main.py"]
