#!/bin/bash
# Sets up your web servers for the deployment of web_static

# Updates the package list & Installs Nginx if it not already installed
sudo apt update
command -v nginx >/dev/null 2>&1 || { sudo apt install -y nginx; }

# Create the folder /data/ if it does not already exist
sudo mkdir -p "/data/"

# Create the folder /data/web_static/ if it does not already exist
sudo mkdir -p "/data/web_static/"

# Create the folder /data/web_static/releases/ if it does not already exist
sudo mkdir -p "/data/web_static/releases/"

# Create the folder /data/web_static/shared/ if it does not already exist
sudo mkdir -p "/data/web_static/shared/"

# Create the folder /data/web_static/releases/test/ if it not exist
sudo mkdir -p "/data/web_static/releases/test/"

# Create a fake HTML file /data/web_static/releases/test/index.html
# (with simple content, to test your Nginx configuration)
sudo touch "/data/web_static/releases/test/index.html"
sudo su
echo "Hello Morocco!" > /data/web_static/releases/test/index.html
exit
# Create a symbolic link /data/web_static/current
# linked to the /data/web_static/releases/test/ folder.
# If the symbolic link already exists, it should be deleted
# and recreated every time the script is ran.
if [ -L "/data/web_static/current" ]; then
    # If it exists, delete it
    sudo rm "/data/web_static/current"
fi
ln -s "$(pwd)/data/web_static/releases/test/" /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group.
# This should be recursive;
# everything inside should be created/owned by this user/group.
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration
# to serve the content of /data/web_static/current/ to hbnb_static
printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location https://www.z-sitawi.tech/hbnb_static {
        alias /data/web_static/current;
        index index.html index.htm;
    }

    location /redirect_me {
        return 301 http://cuberule.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > /etc/nginx/sites-available/default


# Restart Nginx to apply the changes
sudo service nginx restart
