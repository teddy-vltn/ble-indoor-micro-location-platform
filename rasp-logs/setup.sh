
# Check if it's running as root
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root."
    exit
fi

path_to_script="$PWD/main.py"

# Location of the service file
service_file="$PWD/rasplogs.service"

# Check if the service file exists
if [ ! -f "$service_file" ]; then
    echo "rasplogs.service does not exist in the current directory."
    exit
fi

# Replace placeholders in the rasplogs.service file
sed -i "s|%path_to_script%|$path_to_script|g" "$service_file"

echo "Replacements done."

# Check if a rasplogs.service already exists in /lib/systemd/system
if [ -f "/lib/systemd/system/rasplogs.service" ]; then
    # Stop the service
    systemctl stop rasplogs.service

    # Sleep for 5 seconds
    sleep 5

    # Remove the service
    rm /lib/systemd/system/rasplogs.service
fi

# Copy the rasplogs.service file into /lib/systemd/system
cp rasplogs.service /lib/systemd/system/

# Give the rasplogs.service file the correct permissions to root
chown root:root /lib/systemd/system/rasplogs.service

# Reload the systemd daemon
systemctl daemon-reload

echo "rasplogs.service copied into /lib/systemd/system."

# Everything was successful; now delete this script
rm -- "$0"
