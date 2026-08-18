# Use the FuturesSession to make concurrent requests
from requests_futures.sessions import FuturesSession

import datetime
import time
import traceback

from modules.database.utils.cache_utils import add_to_cache, get_from_cache, get_active_profile_id
from modules.database.query.get_active_profile_group import get_active_profile_group
from modules.database.utils.hosts_utils import fetch_host_status, process_host_response

results_of_last_pings = {}
active_hosts_count = 0

# Create a session for concurrent requests
session = FuturesSession(max_workers=50)

def update_inventory_cache(hosts, inventory):
    """
    Update the inventory cache with the latest host statuses.

    Args:
        hosts (dict): A dictionary containing the latest host statuses.
        inventory (dict): The current inventory cache.
    """
    # Iterate over the hosts dictionary
    for key, value in hosts.items():
        # Determine the timestamp of the last successful ping
        timestamp_last_successful_ping = (
            value["timestamp_last_successful_ping"]  # If the host is online
            if value["online"] 
            else inventory.get(key, {}).get("timestamp_last_successful_ping", None)  # If the host is offline, use the existing timestamp if available
        )

        # Update the inventory cache with the latest host status
        inventory[key] = {
            "name": key,  # The name of the host
            "online": value["online"],  # Whether the host is online
            "services": value["services"],  # The state of services running on the host
            "last_pings": value["last_pings"],  # List of last pings
            "timestamp_last_successful_ping": timestamp_last_successful_ping  # Timestamp of the last successful ping
        }

    # Add the updated inventory cache to the cache
    add_to_cache('inventory', inventory)

def update_host_status():
    """
    Continuously update the status of hosts.

    This function runs in an infinite loop, updating the status of hosts in the background.
    It periodically checks for the active profile and raspberry group, and if found, it
    fetches the status of each host and updates the inventory cache accordingly.
    """
    global results_of_last_pings, active_hosts_count

    while True:
        try:
            # Check if there is an active profile
            if not get_active_profile_id():
                print("No active profile found")
                time.sleep(5)
                continue

            # Fetch the active raspberry group and hosts
            group = get_active_profile_group()
            if not group or not group.get('hosts'):
                print("No active raspberry group found" if not group else "No hosts found in the inventory")
                add_to_cache('inventory', {})
                time.sleep(5)
                continue

            # Fetch the status of each host concurrently
            future_requests = [(fetch_host_status(session, host_data['name']), host_data['name']) for host_data in group['hosts'] if host_data]
            hosts = {}
            _active_hosts_count = 0

            for future, host in future_requests:
                # Process the response from the host status request
                online, service_status = process_host_response(future, host)
                _active_hosts_count += 1 if online else 0

                if host not in results_of_last_pings:
                    results_of_last_pings[host] = []
                results_of_last_pings[host].append(online)
                if len(results_of_last_pings[host]) > 5:
                    results_of_last_pings[host].pop(0)

                hosts[host] = {
                    "online": online,
                    "services": service_status,
                    "last_pings": results_of_last_pings[host],
                    # Set the timestamp of the last successful ping if the host is online
                    "timestamp_last_successful_ping": datetime.datetime.now().timestamp() if online else None
                }

            # Update the inventory cache with the latest host statuses
            inventory = get_from_cache('inventory')
            update_inventory_cache(hosts, inventory)
            active_hosts_count = _active_hosts_count
            time.sleep(5)

        except Exception as e:
            # Print the error and wait for 5 seconds before retrying
            print(f"Error: {e}")
            tb = traceback.format_exc()
            print(tb)
            time.sleep(5)
