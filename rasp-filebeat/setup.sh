#!/bin/bash

# Check if it's running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root."
    exit
fi

filebeat_archive_name="filebeat-7.15.2-linux-armv6l"
filebeat_archive="$filebeat_archive_name.tar.gz"

# Define the actual paths
filebeat_executable_path="$PWD/filebeat/filebeat"
filebeat_config_path="$PWD/filebeat/filebeat.yml"

# Location of the filebeat service file
service_file="$PWD/filebeat.service"

# Check if the filebeat archive exists
if [ -f $filebeat_archive ]; then

    # Extract the archive
    echo "Extracting $filebeat_archive..."
    tar -zxvf $filebeat_archive

    # Rename the extracted directory
    echo "Renaming the extracted directory to filebeat..."
    mv $filebeat_archive_name filebeat

    # Check if the filebeat.yml file exists
    if [ -f "filebeat.yml" ]; then
        # Move the filebeat.yml into the extracted directory
        echo "Moving filebeat.yml into the extracted directory..."
        mv filebeat.yml filebeat/

        # Give the filebeat.yml file the correct permissions to root
        chown root:root filebeat/filebeat.yml
    else
        echo "filebeat.yml does not exist in the specified directory."
    fi

    # Check if a service already exists in /lib/systemd/system for filebeat.service
    if [ -f "/lib/systemd/system/filebeat.service" ]; then
        # Stop the service
        echo "Stopping filebeat service..."
        systemctl stop filebeat.service

        # Sleep for 5 seconds
        echo "Sleeping for 5 seconds... This is to ensure the service is stopped."
        sleep 5

        # Remove the service
        rm /lib/systemd/system/filebeat.service
    fi

    # Replace placeholders in the filebeat.service file
    sed -i "s|%filebeat_executable_path%|$filebeat_executable_path|g" "$service_file"
    sed -i "s|%filebeat_config_path%|$filebeat_config_path|g" "$service_file"

    # Copy the filebeat.service file into /lib/systemd/system
    echo "Copying filebeat.service into /lib/systemd/system..."
    cp filebeat.service /lib/systemd/system/

    # Check if the filebeat.service file exists in /lib/systemd/system
    if [ -f "/lib/systemd/system/filebeat.service" ]; then
        # Give the filebeat.service file the correct permissions to root
        chown root:root /lib/systemd/system/filebeat.service
    else
        echo "filebeat.service does not exist in the specified directory."
    fi

    # Enable the service
    echo "Enabling filebeat service..."
    systemctl enable filebeat.service

    # Start the service
    echo "Starting filebeat service..."
    systemctl start filebeat.service

    # Check if everyrhing was successful
    if [ $? -eq 0 ]; then

        echo "Everything was successful. Deleting artifacts..."

        # Remove the tar file
        rm $filebeat_archive

        # Remove the filebeat.service
        rm filebeat.service

        # Everything was successful; now delete this script
        rm -- "$0"

        echo "Artifacts deleted. Exiting..."
    else
        echo "Failed to start filebeat service."
    fi

else
    echo "$filebeat_archive does not exist in the specified directory."
fi
