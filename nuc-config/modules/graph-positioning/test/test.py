import os
import sys

g_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(g_path)

import lib.model as model
from lib.trajectory import PlayerNetworkPath
import lib.reader as reader
import time
import json

from lib.util.load_config import load_config

config = load_config()

dataset = config['test_dataset']

m = model.ModelNetwork(file=g_path + '/data/' + dataset + '/model.gml')

#p = reader.RaspberryPiDataReader(file='data/raspberry.json')
r = reader.BeaconDataReader(
    file=g_path + '/data/' + dataset + '/beacons.json',
    #rasp_data=p.data
)

for _, beacon_data in r.beacons_data.items():

    print("Processing beacon data for minor: ", beacon_data.minor)

    ts = time.time()

    p = PlayerNetworkPath(beacon_data, m)

    p.load_settings( definition={
        'AVERAGE_RSSI_WEIGHT': 0.80, 
        'BEACON_COUNT_WEIGHT': 0.25, 
        'CONFIDENCE_THRESHOLD': 0.5,
        'DISTANCE_WEIGHT': 0.248, 
        'RSSI_MIN': -90,
        'RSSI_MAX': -75,
        'DISTANCE_MAX': 3.5,
        'DISTANCE_MIN': 0.1,
    }, time_interval_of_groups=8, debug=False)

    result = p.move_in_network()
    
    # dump json into a file for every player data
    with open(g_path + '/data/musee/player_data.txt', 'a') as f:
        json.dump(result.temporal_sequence_visited, f)
        # New line for the next player data
        f.write('\n')






