FROM python:3.9-alpine

# Install packages
#RUN apk add --no-cache python3 py3-pip augeas-libs certbot nginx && rm -rf /var/cache/apk/*

# make pip also use piwheels
ADD pip.conf /etc/pip.conf

EXPOSE 80
ENV PORT=80

# Create app environment
RUN mkdir /app
WORKDIR /app
ENV PYTHONUNBUFFERED=true

# Install Packages
ADD requirements.txt .
RUN pip install --upgrade --no-cache-dir -r requirements.txt

# Start service
ENTRYPOINT ["/bin/sh", "start-service.sh"]

# add source files
ENV SOURCE_CODE="/app"
ADD LICENSE .
ADD Dockerfile .
ADD start-service.sh .

# Add the app
ADD app.py .
