from bson import ObjectId
import datetime
from modules.database.utils.cache_utils import get_active_profile_id
from modules.database.query.get_active_profile_group import get_active_profile_group
from modules.database.database import db

def create_document_ansible_log(script_name, start_time, output):

    active_profile_id = get_active_profile_id()
    group = get_active_profile_group()
    
    if group:
        # Get only the host with a .active field set to True
        hosts = [host['name'] for host in group['hosts'] if host.get('active', False)]

    log_entry = {
        'profile_id': ObjectId(active_profile_id),
        'script_name': script_name,
        'start_time': start_time,
        'output': output,
        'stop_time': datetime.datetime.now().timestamp(),
        'hosts': hosts,
    }
    db.script_logs.insert_one(log_entry)

def find_all_ansible_logs():
    active_profile_id = get_active_profile_id()

    # Find the last 20 logs for the active profile and sort them by start_time
    logs = list(db.script_logs.find({'profile_id': ObjectId(active_profile_id)}, {'profile_id': 0, '_id': 0}).sort('start_time', -1).limit(20))

    return logs

def duplicate_all_ansible_logs(profile_id_to_duplicate, new_profile_id):
    logs = list(db.script_logs.find({'profile_id': ObjectId(profile_id_to_duplicate)}))
    for log in logs:
        log['profile_id'] = ObjectId(new_profile_id)
        db.script_logs.insert_one({
            'profile_id': log['profile_id'],
            'script_name': log['script_name'],
            'start_time': log['start_time'],
            'output': log['output'],
            'stop_time': log['stop_time'],
            'hosts': log['hosts']
        })
        