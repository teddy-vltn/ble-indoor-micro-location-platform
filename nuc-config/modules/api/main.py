import sys
import os
from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from modules.database.database import db

from lib.create_app import create_app

app, socketio = create_app()

import threading

from flask_socketio import emit

from modules.api.lib.task.background_task import update_host_status

thread = threading.Thread(target=update_host_status)
thread.daemon = True
thread.start()

from modules.database.utils.cache_utils import get_from_cache
from lib.ansible_manager import execute_ansible_playbook

@socketio.on('connect', namespace='/bash')
def on_connect():
    # get all the scripts
    scripts = get_from_cache("ansible_scripts")

    if scripts:
        emit('scripts_list', {'scripts': scripts})

@socketio.on('start_script', namespace='/bash')
def handle_start_script(message):
    script_name = message.get('script_name', '')
    if script_name:
        execute_ansible_playbook(socketio, script_name)

if __name__ == '__main__':
    port = int(os.getenv('API_PORT', 5001))
    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True)
