# Stage 1: Nginx and Flask Server
FROM ubuntu:latest AS base

# Install required packages
RUN apt-get update && apt-get install -y curl gnupg2 ca-certificates lsb-release ubuntu-keyring nginx 

# Import Nginx signing key and add Nginx repository
RUN curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor \
    | tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null
RUN printf "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
    http://nginx.org/packages/ubuntu %s nginx\n" \
    "$(lsb_release -cs)" | tee /etc/apt/sources.list.d/nginx.list >/dev/null

# Install Nginx and NJS module
RUN apt-get update && apt-get install -y nginx nginx-module-njs

# Copy your Nginx configuration file that includes the njs code to the Docker image
COPY nginx.conf /etc/nginx/nginx.conf
COPY default.conf /etc/nginx/conf.d/default.conf

# Copy your application code to the Docker image
COPY . /waf/

# Expose the necessary ports
EXPOSE 80

# Start both Nginx and Flask servers in the background when the container starts
CMD ["sh", "-c", "nginx -g 'daemon off;'"]
