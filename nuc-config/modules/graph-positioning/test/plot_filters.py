import numpy as np
import matplotlib.pyplot as plt
import os
import sys

g_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(g_path)

from lib.reader import BeaconDataReader
from lib.util.load_config import load_config

config = load_config()

dataset = config['test_dataset']

sys.path.append(g_path)

# Exemple des valeurs RSSI brutes
r = BeaconDataReader(file=g_path + '/data/' + dataset + '/beacons.json')

def moving_average(values, window=10):
    weights = np.ones(window) / window
    return np.convolve(values, weights, mode='valid')

def kalman_filter_rssi(rssi_values, Q=1, R=30):
    x_estime = np.array([[rssi_values[0]]])  # État initial: RSSI initial
    P = np.array([[1]])                      # Covariance initiale de l'état
    F = np.array([[1]])                      # Matrice de transition d'état
    H = np.array([[1]])                      # Matrice de mesure
    filtered_rssi = [x_estime.item()]
    
    for rssi in rssi_values[1:]:
        x_pred = F @ x_estime
        P_pred = F @ P @ F.T + Q
        
        K = P_pred @ H.T @ np.linalg.inv(H @ P_pred @ H.T + R)
        x_estime = x_pred + K @ (rssi - H @ x_pred)
        P = (np.eye(1) - K @ H) @ P_pred
        
        filtered_rssi.append(x_estime.item())
        
    return filtered_rssi


for _, beacon_data in r.beacons_data.items():
    print("-------------------")
    print("Processing beacon data for minor: ", beacon_data.minor)
    rssi_values = [d['rssi'] for d in beacon_data.data]

    all_hosts = set([d['hostname'] for d in beacon_data.data])

    host_kalman = {}
    host_moving_average = {}
    host_rssi = {}

    for host in all_hosts:
        _host_rssi = [d['rssi'] for d in beacon_data.data if d['hostname'] == host]
        host_rssi[host] = _host_rssi

        host_kalman[host] = kalman_filter_rssi(_host_rssi)
        host_moving_average[host] = moving_average(_host_rssi, window=10)

    # subplot for each host
    MAX_HOST_PLOT = 4
    fig, axs = plt.subplots(MAX_HOST_PLOT, 1, figsize=(10, 5))
    fig.suptitle('RSSI values for minor: ' + str(beacon_data.minor))

    for i, host in enumerate(all_hosts):
        if i >= MAX_HOST_PLOT:
            break
        axs[i].plot(host_rssi[host], label='Raw RSSI')
        axs[i].plot(host_kalman[host], label='Kalman filter', color='red')
        axs[i].plot(host_moving_average[host], label='Moving average', color='green')
        # make sure host is a string
        host = str(host)
        axs[i].set_title('RSSI values for host: ' + host )
        #axs[i].legend()
    plt.show()




