-- Check if the database exists, create it if it doesn't
CREATE DATABASE IF NOT EXISTS hbnb_dev_db;

-- Check if the user exists, create it if it doesn't
CREATE USER IF NOT EXISTS 'hbnb_dev'@'localhost' IDENTIFIED BY 'hbnb_dev_pwd';

-- Grant USAGE privilege to the user
GRANT USAGE ON *.* TO 'hbnb_dev'@'localhost';

-- Grant SELECT privilege on performance_schema database
GRANT SELECT ON performance_schema.* TO 'hbnb_dev'@'localhost';

-- Grant all privileges on the hbnb_dev_db database
GRANT ALL PRIVILEGES ON hbnb_dev_db.* TO 'hbnb_dev'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;
