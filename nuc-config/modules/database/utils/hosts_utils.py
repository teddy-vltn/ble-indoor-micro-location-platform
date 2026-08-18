from modules.database.query.get_active_profile_group import get_active_profile_group
from modules.database.utils.cache_utils import add_to_cache, get_from_cache

def refresh_hosts_cache():
    """Refresh the hosts cache."""
    group = get_active_profile_group()
    hosts = group.get('hosts', {})
    add_to_cache('hosts', hosts)

def remove_ghost_hosts():
    """Remove hosts from the inventory that are no longer present in the active raspberry group."""
    inventory = get_from_cache("inventory")
    groups = get_active_profile_group()
    new_hosts = groups['hosts'] if groups['hosts'] else []
    names_new_hosts = [host['name'] for host in new_hosts]
    to_delete = [key for key in inventory.keys() if key not in names_new_hosts]

    for key in to_delete:
        del inventory[key]

    add_to_cache('inventory', inventory)

def fetch_host_status(session, host):
    """
    Fetch the status of a given host.

    Args:
        session (requests.Session): The session object to use for the request.
        host (str): The host to fetch the status from.

    Returns:
        requests.Response: The response object containing the status of the host.
    """
    # Construct the URL to fetch the status from.
    # The URL includes the host and the names of the services to check.
    url = f'http://{host}:5000/status?service_name=filebeat&service_name=rasplogs'
    
    # Send a GET request to the URL with a timeout of 3 seconds.
    return session.get(url, timeout=3)

services_to_check = ["rasplogs", "filebeat"]

def process_host_response(future, host):
    """
    Process the response from a host status request.

    Args:
        future (concurrent.futures.Future): The future object representing the
            response from the host status request.
        host (str): The host to process the response for.

    Returns:
        Tuple[bool, Dict[str, Optional[bool]]]: A tuple containing a boolean
        indicating whether the host is online and a dictionary with the status
        of the services running on the host. The dictionary has the service
        names as keys and the status as values. If the service is running, the
        value is True, if it is not running, the value is False, and if the
        service status is uncertain, the value is None.
    """
    try:
        # Get the response from the future object.
        r = future.result()
        online = r.status_code == 200
        service_status = r.json() if online else {}

        # Transform the 'active' and 'inactive' keys into booleans.
        for service, status in service_status.items():
            service_status[service] = status == 'active'

        # Print a message indicating whether the host is online.
        print(f"{host} is online: {online}")

    # If an exception occurred, set the online status to False and set the
    # service status to None for all services.
    except Exception:
        online = False
        service_status = {service: None for service in services_to_check}

    # Return the online status and the service status.
    return online, service_status
