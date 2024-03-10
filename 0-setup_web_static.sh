#!/bin/bash
# Sets up your web servers for the deployment of web_static

# Updates the package list & Installs Nginx if it not already installed
sudo apt update
command -v nginx >/dev/null 2>&1 || { sudo apt install -y nginx; }

# Create the folder /data/ if it does not already exist
mkdir -p "./data/"

# Create the folder /data/web_static/ if it does not already exist
mkdir -p "./data/web_static/"

# Create the folder /data/web_static/releases/ if it does not already exist
mkdir -p "./data/web_static/releases/"

# Create the folder /data/web_static/shared/ if it does not already exist
mkdir -p "./data/web_static/shared/"

# Create the folder /data/web_static/releases/test/ if it not exist
mkdir -p "./data/web_static/releases/test/"

# Create a fake HTML file /data/web_static/releases/test/index.html
# (with simple content, to test your Nginx configuration)
touch "./data/web_static/releases/test/index.html"
echo "Hello Morocco!" > ./data/web_static/releases/test/index.html

# Create a symbolic link /data/web_static/current
# linked to the /data/web_static/releases/test/ folder.
# If the symbolic link already exists, it should be deleted
# and recreated every time the script is ran.
if [ -L "/data/web_static/current" ]; then
    # If it exists, delete it
    rm "/data/web_static/current"
fi
ln -s "$(pwd)/data/web_static/releases/test/" /data/web_static/current

# Give ownership of the /data/ folder to the ubuntu user AND group.
# This should be recursive;
# everything inside should be created/owned by this user/group.
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration
# to serve the content of /data/web_static/current/ to hbnb_static
CONFIG_FILE="/etc/nginx/sites-available/default"
# Add or update the location block inside the server block
sudo tee -a "$CONFIG_FILE" > /dev/null <<EOF

        location https://www.z-sitawi.tech/hbnb_static {
            alias /data/web_static/current/;
        }
EOF

# Restart Nginx to apply the changes
sudo service nginx restart
