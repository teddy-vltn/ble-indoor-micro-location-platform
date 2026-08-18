import json
from datetime import datetime

class RaspberryPiData:
    """
    RaspberryPiData: Classe pour stocker les données des Raspberry Pi.

    Attributs:
        hostname (str): Le nom d'hôte du Raspberry Pi.
        node (str): Le lieu du Raspberry Pi.
    """
    def __init__(self, hostname, node):
        self.hostname = hostname
        self.node = node

class RaspberryPiDataReader:
    def __init__(self, collection=None, file=None):
        self.data = self.load_from_file(file) if file is not None else self.load_from_collection(collection)

    def load_from_collection(self, collection):
        processed = {}

        for hostname, node in collection.items():
            # check if there is .local in hostname
            # if there is remove it
            if ".local" in hostname:
                hostname = hostname.split(".")[0]
            processed[hostname] = RaspberryPiData(hostname, node)

        return processed

    def load_from_file(self, file):
        processed = {}

        with open(file) as f:
            data = json.load(f)

        for key, value in data.items():
            processed[key] = RaspberryPiData(key, value)

        return processed

class BeaconData:
    """
    BeaconData: Classe pour stocker les données des beacons.

    Attributs:
        data (list): Les données des beacons.
        minor (int): L'identifiant minor du beacon.
    """
    def __init__(self, data, minor):
        self.minor = minor
        self.data = data



class BeaconDataReader:
    """
    BeaconDataReader: Classe pour lire les données des beacons.

    Attributs:
        isFile (bool): Indique si les données sont lues à partir d'un fichier.
        file (str): Le fichier contenant les données des beacons.
        dataset (dict): Les données des beacons.
        data (list): Les données des beacons.
        beacons_data (dict): Les données des beacons séparées par minor.

    Méthodes:
        generate_data: Génère les données des beacons séparées par minor.
        read_file: Lit les données des beacons à partir d'un fichier.
        read_data: Lit les données des beacons.
        clean_data: Nettoie les données des beacons.
    """
    def __init__(self, file = None, data = None, rasp_data = None):
        self.isFile = False if file is None else True
        self.file = file

        self.rssi_max = -75
        self.rssi_min = -90

        self.dataset = data
        self.rasp_data = rasp_data
        self.data = self.read_data()

        self.beacons_data = self.generate_data()

    def generate_data(self):
        # Separate data by minor
        data = self.data
        beacons_data = {}
        for d in data:
            minor = d.get("minor") 

            if minor is None:
                continue

            if minor not in beacons_data:
                beacons_data[minor] = BeaconData([], minor)
            
            beacons_data[minor].data.append(d)

        return beacons_data
    
    def read_file(self):
        with open(self.file) as f:
            data = json.load(f)

        return data

    def read_data(self, sort_by = "timestamp"):
        # Data is in json format
        if self.isFile:
            data = self.read_file()
        else:
            data = self.dataset

        data = self.clean_data(data)
        # Sort data by date
        data = sorted(data, key = lambda x: x.get(sort_by))
        return data
    
    def clean_data(self, data):
        cleaned_data = []

        for d in data: 
            rssi = d.get("rssi")

            if d.get("hostname") is None:
                continue

            if rssi > self.rssi_max:
                self.rssi_max = rssi

            if rssi < self.rssi_min:
                self.rssi_min = rssi

            hostname = d.get("hostname")

            if self.rasp_data is not None:
                hostname = self.rasp_data.get(d.get("hostname"))
                if hostname is None:
                    hostname = "Unknown"
                else:
                    hostname = hostname.node

            cleaned_data.append( 
               {
                   "rssi": rssi,
                   "major": d.get("major"),
                   "minor": d.get("minor"),
                   "tx_power": d.get("tx_power"),
                   "hostname": hostname,
                   "timestamp": d.get("timestamp")
               }
            ) 

        return cleaned_data
    