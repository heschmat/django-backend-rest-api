FROM python:3.13-alpine3.20
LABEL maintainer="heschmatx@gmail.com"

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    linux-headers

# Create virtual environment and install dependencies
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp

# Set PATH to include the virtual environment
ENV PATH="/py/bin:$PATH"

# Copy application files
COPY ./app /app
WORKDIR /app

# Create and use a non-root user
RUN adduser --disabled-password --no-create-home user1
RUN chown -R user1:user1 /app
USER user1

# Expose the application port
EXPOSE 8000
