FROM python:3.9-alpine

# Create app directory
WORKDIR /usr/src/app
COPY package*.json ./

# Expose Ports
ENV PORT 8080
EXPOSE 8080

# Install libraries
COPY . .
RUN pip3 install -qr requirements.txt


CMD ["sls", "wsgi", "serve"]