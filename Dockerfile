FROM python:3.13-alpine3.20
LABEL maintainer="heschmatx@gmail.com"

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    linux-headers

# copy the requirements (including dev requirements) to /tmp
COPY ./requirements.txt ./requirements.dev.txt /tmp/


# Copy application files
# the **contents** of `app` in local into the /app directory.
COPY ./app /app
WORKDIR /app

ARG DEV=false

# Set PATH to include the virtual environment
# /py/bin is being prepended to the PATH variable
# now we can simply use `pip` rather than `/py/bin/pip`
ENV PATH="/py/bin:$PATH"

# Create virtual environment and install dependencies
RUN python -m venv /py && pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser --disabled-password --no-create-home user1 && \
    chown -R user1:user1 /app

USER user1

# Expose the application port
EXPOSE 8000
