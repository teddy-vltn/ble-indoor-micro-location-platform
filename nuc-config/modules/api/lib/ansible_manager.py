import os
import datetime
import ansible_runner

from dotenv import load_dotenv

load_dotenv()

import yaml

config_absolute_path = os.getenv('CONFIG_ABSOLUTE_PATH')

def load_config():
    with open(config_absolute_path, 'r') as file:
        config = yaml.safe_load(file)
    return config['ansible-playbooks']

from modules.database.utils.cache_utils import add_to_cache, get_from_cache
from modules.database.utils.ansible_utils import create_document_ansible_log

ANSIBLE_PLAYBOOKS = load_config()
            
last_script_output = ""
socketio = None

def custom_event_handler(event_data):
    """
    Handle the custom event data and emit the bash output.

    Args:
        event_data (dict): The event data containing stdout.
    """
    global last_script_output
    # Check if stdout is present in the event data
    if (dump := event_data.get('stdout')):
        # Split the dump into lines and append each line to the last_script_output
        for line in dump.splitlines():
            last_script_output += line + '\n'
            # Emit the bash output with the line to the socketio namespace '/bash'
            socketio.emit(
                'bash_output',
                {'data': line + '\n'},
                namespace='/bash'
            )

def finished_callback(status, runner_config=None):
    print('Playbook execution finished.')
    print(status)

def execute_ansible_playbook(_socketio, playbook_key):
    """
    Executes an Ansible playbook based on the playbook key.

    Args:
        _socketio (SocketIO): The SocketIO object for emitting events.
        playbook_key (str): The key of the playbook to be executed.

    Returns:
        None
    """
    global last_script_output
    global socketio

    socketio = _socketio
    start_time = datetime.datetime.now().timestamp()

    # Print active directory
    socketio.emit('bash_output', {'data': f"Active directory: {os.getcwd()}\n"}, namespace='/bash')

    # Get the playbook group based on the playbook key
    playbook_group = ANSIBLE_PLAYBOOKS.get(playbook_key)
    if not playbook_group:
        error_message = 'Playbook group not found.\n'
        socketio.emit('bash_output', {'data': error_message}, namespace='/bash')
        create_document_ansible_log(playbook_key, start_time, error_message)
        return

    # Build inventory from cache
    inventory = build_inventory_from_cache()

    for key in sorted(playbook_group['playbooks'].keys()):
        playbook = playbook_group['playbooks'][key]
        playbook_path = playbook['path']
        playbook_vars = playbook.get('vars', {})

        # Check if gitlab_access_token is to true
        if playbook_vars.get('gitlab_access_token', False):
            gitlab_access_token = os.getenv('GITLAB_ACCESS_TOKEN')
            if not gitlab_access_token:
                error_message = 'Gitlab access token not set.\n'
                socketio.emit('bash_output', {'data': error_message}, namespace='/bash')
                create_document_ansible_log(playbook_key, start_time, error_message)
                return

            playbook_vars['gitlab_access_token'] = gitlab_access_token
        
        if not os.path.isfile(playbook_path):
            error_message = 'Playbook does not exist.\n'
            socketio.emit('bash_output', {'data': error_message}, namespace='/bash')
            create_document_ansible_log(playbook_key, start_time, error_message)
            return

        try:
            # Run the Ansible playbook
            r = ansible_runner.run(
                private_data_dir='.', 
                playbook=playbook_path, 
                inventory=inventory, 
                extravars=playbook_vars, 
                event_handler=custom_event_handler,
                status_handler=finished_callback
            )

        except Exception as e:
            error_message = f"An error occurred: {str(e)}\n"
            socketio.emit('bash_output', {'data': error_message}, namespace='/bash')
            create_document_ansible_log(playbook_key, start_time, error_message)
            return
        
    socketio.emit('bash_output', {'data': '\n\nPlaybook execution finished.\n'}, namespace='/bash')

    create_document_ansible_log(playbook_key, start_time, last_script_output)

    # Reset last_script_output
    last_script_output = ""

def set_ansible_playbook_cache():
    a = ANSIBLE_PLAYBOOKS

    b = {}
    # Only extract the name and description of the playbooks
    for key in a.keys():
        # a[key] is a playbook group
        # Just get name and description of that key
        b[key] = {
            'name': a[key]['name'],
            'description': a[key]['description']
        }

    add_to_cache('ansible_scripts', b)

def build_inventory_from_cache() -> str:
    """
    Builds an inventory string from the hosts cache.

    Returns:
        str: The inventory string in the format expected by ansible_runner.
    """
    # Get hosts from the cache
    hosts_cache = get_from_cache('hosts')

    # Filter active hosts
    active_hosts = [host['name'] for host in hosts_cache if host['active']]

    def add_user_and_pass(host: str) -> str:
        """
        Adds the user and password to the host.

        Args:
            host (str): The host name.

        Returns:
            str: The host with the user and password added.
        """
        ansible_ssh_user = os.getenv('DEVICES_SSH_USER')
        ansible_ssh_pass = os.getenv('DEVICES_SSH_PASS')
        return f"{host} ansible_ssh_user={ansible_ssh_user} ansible_ssh_pass={ansible_ssh_pass}"

    # Build the inventory string in the format expected by ansible_runner
    inventory = '\n'.join([add_user_and_pass(host) for host in active_hosts])

    # Add group name in the inventory string
    inventory = f"[raspberry]\n{inventory}\n"

    return inventory

set_ansible_playbook_cache()
