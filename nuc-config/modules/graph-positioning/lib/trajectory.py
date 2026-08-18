import networkx as nx
import sys
sys.path.append("../")
from .kalman import kalman_filter_rssi

DATE_KEY = "timestamp"

from lib.util.load_config import load_config

# Read configuration file
config = load_config()
    
class PlayerTrace:
    def __init__(self, has_visited_beacons, last_visited_beacon, last_data_time, temporal_sequence_visited):
        self.has_visited_beacons = has_visited_beacons
        self.last_visited_beacon = last_visited_beacon
        self.last_data_time = last_data_time
        self.temporal_sequence_visited = temporal_sequence_visited

class PlayerNetworkPath:
    """
    Classe représentant le chemin réseau d'un joueur à travers les beacons détectés.
    
    Attributs:
        model_network (NetworkX Graph): Le modèle de réseau représentant les connexions entre les beacons.
        last_visited_beacon (int): Le dernier beacon visité par le joueur.
        beacons_data (dict): Les données des beacons détectées par le joueur.
        minor (int): L'identifiant minor du beacon.
        has_visited_beacons (list): La liste des beacons déjà visités par le joueur.
        last_data_time (datetime): La dernière fois que les données ont été reçues.
        temporal_sequence_visited (dict): La séquence temporelle des beacons visités.
        grouped_data_time (list): Les données des beacons groupées en fonction de leur fenêtre temporelle.
        
    Méthodes:
        get_data_time_range: Retourne la plage de dates des données des beacons.
        group_data_based_on_time_window: Groupe les données des beacons en fonction d'une fenêtre temporelle.
        validate_group_data: Valide un groupe de données en fonction d'un critère spécifique (ex. longueur).
        get_best_candidate: Sélectionne le meilleur beacon candidat à partir d'un groupe de données.
        get_frequency_in_group: Calcule la fréquence d'apparition des beacons dans un groupe.
        kalman_filter_rssi: Applique un filtre de Kalman pour lisser les valeurs RSSI.
        smooth_rssi_values: Lisse les valeurs RSSI des beacons dans un groupe.
        distances_from_last_visited: Calcule les distances depuis le dernier beacon visité pour chaque beacon dans un groupe.
        move_in_network: Déplace le joueur dans le réseau en fonction des meilleurs chemins calculés.
    """
    def __init__(self, 
                 beacon_data, 
                 model_network, 
                 has_visited_beacons=None, 
                 last_visited_beacon=None):
        
        self.model_network = model_network
        self.last_visited_beacon = last_visited_beacon if last_visited_beacon is not None else None
        self.beacons_data = beacon_data.data
        self.minor = beacon_data.minor
        self.has_visited_beacons = has_visited_beacons if has_visited_beacons is not None else []
        self.last_data_time = None
        self.temporal_sequence_visited = {}
        self.last_movement_time = None

    def get_data_time_range(self):
        """
            Return the time range of the beacons data.

            :return: The time range of the beacons data. tuple (start, end)
        """
        return self.beacons_data[0][DATE_KEY], self.beacons_data[-1][DATE_KEY]
    
    def load_settings(self, definition=None, time_interval_of_groups=None, debug=None, default_settings=False):
        """
            Load the settings for the player network path.

            :param definition: The definition of the trajectory parameters.
            :param time_interval_of_groups: The time interval of the groups.
            :param debug: The debug mode.
            :param default_settings: The default settings.
        """
        if default_settings:
            definition = config["trajectory_parameters"]
            time_interval_of_groups = config["time_interval_of_groups"]
            debug = config["trajectory_debug"]

        for key, value in definition.items():
            setattr(self, key.upper(), value)

        self.time_interval_of_groups = time_interval_of_groups
        self.debug = debug

    def group_data_based_on_time_window(self, time_window):
        """
            Group the data based on a time window. Every group contains data from the same time window.

            :param time_window: The time window to group the data.
            :return: The grouped data.
        """
        print("Grouping data based on time window of ", time_window)
        grouped_data = []
        current_group = [self.beacons_data[0]]
        for data in self.beacons_data[1:]:
            difference_unix_timestamp = float(data[DATE_KEY]) - float(current_group[0][DATE_KEY]) 
            if (difference_unix_timestamp) <= time_window:
                current_group.append(data)
            else:
                if self.validate_group_data(current_group):
                    grouped_data.append(current_group)
                current_group = [data]

        self.last_data_time = grouped_data[-1][-1][DATE_KEY] if grouped_data else None
        print("Last data time: ", self.last_data_time)
        return [group for group in grouped_data if self.validate_group_data(group)]

    @staticmethod
    def validate_group_data(group):
        """
            Validate a group of data based on a specific criterion (ex. length).

            :param group: The group of data.
            :return: True if the group is valid, False otherwise.
        """
        return len(group) > 10

    def get_best_candidate(self, group):
        """
            Select the best candidate beacon from a group of data.

            :param group: The group of data.
            :return: The best candidate beacon, the score of the candidate, and the raw score if debug mode is enabled.
        """
        beacon_count = self.get_frequency_in_group(group)
        average_rssi = self.smooth_rssi_values(group)

        distances = {}
        normalized_scores = {}

        if self.last_visited_beacon != None:
            distances = self.distances_from_last_visited(group)
        
        raw_score = {}

        for key in beacon_count:
            if self.debug:
                raw_score[key] = {"rssi": average_rssi[key], "count": beacon_count[key], "distance": distances.get(key, 0)}
            normalized_scores[key] = (self.AVERAGE_RSSI_WEIGHT * average_rssi[key] + self.BEACON_COUNT_WEIGHT * beacon_count[key] - self.DISTANCE_WEIGHT * distances.get(key, 0))
            #print("Beacon: ", key, " RSSI: ", round(average_rssi[key], 2), " Count: ", round(beacon_count[key], 2), " Distance: ", round(distances.get(key, 0), 2), " Score: ", round(normalized_scores[key], 2))
            
        best_candidate = max(normalized_scores, key=normalized_scores.get)
        best_candidate_score = normalized_scores[best_candidate]
        return best_candidate, best_candidate_score, raw_score[best_candidate] if self.debug else None

    @staticmethod
    def get_frequency_in_group(group):
        """
            Compute the frequency of appearance of the beacons in a group.

            :param group: The group of data.
            :return: The frequency of appearance of the beacons.
        """
        beacon_count = {}
        for d in group:
            beacon_count[d["hostname"]] = beacon_count.get(d["hostname"], 0) + 1

        min_count = min(beacon_count.values())
        max_count = max(beacon_count.values()) + 1e-6

        for key in beacon_count:
            beacon_count[key] = (beacon_count[key] - min_count) / (max_count - min_count)

        return beacon_count
    
    def limit_rssi(self, rssi):
        """
            Limit the RSSI value to a range.

            :param rssi: The RSSI value.
            :return: The limited RSSI value.
        """
        # closer to RSSI_MIN is 0, closer to RSSI_MAX is 1
        return (rssi - self.RSSI_MIN) / (self.RSSI_MAX - self.RSSI_MIN)

    def smooth_rssi_values(self, group):
        """
            Smooth the RSSI values of the beacons in a group. 
            Use Kalman filter to smooth the RSSI values.

            :param group: The group of data.
            :return: The smoothed RSSI values.
        """
        rssi_values = {}
        for d in group:
            rssi_values.setdefault(d["hostname"], []).append(d["rssi"])

        # Kalman filter RSSI values
        smoothed_rssi = {}
        for key in rssi_values:
            if smoothed_rssi.get(key) is None:
                smoothed_rssi[key] = []
            
            smoothed_rssi[key].extend(kalman_filter_rssi(rssi_values[key]))

        # Average the RSSI values
        for key in smoothed_rssi:
            smoothed_rssi[key] = sum(smoothed_rssi[key]) / len(smoothed_rssi[key])

        # Normalize the RSSI values
        for key in smoothed_rssi:
            smoothed_rssi[key] = self.limit_rssi(smoothed_rssi[key])

        return smoothed_rssi
    
    def limit_distance(self, distance):
        """
            Limit the distance value to a range.

            :param distance: The distance value.
            :return: The limited distance value.
        """
        # closer to DISTANCE_MIN is 0, closer to DISTANCE_MAX is 1
        return (distance - self.DISTANCE_MIN) / (self.DISTANCE_MAX - self.DISTANCE_MIN)

    def distances_from_last_visited(self, group):
        """
            Compute the distances from the last visited beacon for each beacon in a group.

            :param group: The group of data.
            :return: The distances from the last visited beacon.
        """
        distances = {}
        for d in group:
            try:
                distances[d["hostname"]] = nx.dijkstra_path_length(self.model_network.graph, 
                                                        str(self.last_visited_beacon), 
                                                        str(d["hostname"])) - 1
            except nx.NetworkXNoPath:
                distances[d["hostname"]] = 1000
            
        for key in distances:
            distances[key] = self.limit_distance(distances[key]) 

        return distances 

    def move_in_network(self):
        """
            Move the player in the network based on the best calculated paths for each group of data.

            :return: The player trace.
        """
        for group in self.group_data_based_on_time_window(self.time_interval_of_groups):
            best_candidate, best_candidate_score, _ = self.get_best_candidate(group)
            best_candidate = str(best_candidate)

            print("Best candidate: ", best_candidate, " with a score of ", best_candidate_score)

            if best_candidate_score < self.CONFIDENCE_THRESHOLD:
                continue

            if self.last_visited_beacon != None:
                shortest_path = nx.dijkstra_path(self.model_network.graph, 
                                                str(self.last_visited_beacon if self.last_visited_beacon else self.has_visited_beacons[-1]), 
                                                best_candidate)
            else:
                shortest_path = [best_candidate]

            self.has_visited_beacons.extend([node for node in shortest_path if node not in self.has_visited_beacons])

            if ((self.last_visited_beacon == None or self.last_visited_beacon != best_candidate) or self.debug):
                print("Moving from ", self.last_visited_beacon, " to ", best_candidate, " at ", group[-1][DATE_KEY], " with a score of ", round(best_candidate_score, 2))
                date_to_string = group[-1][DATE_KEY]
                self.temporal_sequence_visited[str(date_to_string)] = {
                    "from": self.last_visited_beacon,
                    "to": shortest_path[1:] if len(shortest_path) > 1 else [best_candidate],
                    "score": best_candidate_score if not self.debug else _
                }

            self.last_visited_beacon = best_candidate

        print("Last visited: ", self.last_visited_beacon, self.has_visited_beacons, self.last_data_time)

        return PlayerTrace(self.has_visited_beacons, self.last_visited_beacon, self.last_data_time, self.temporal_sequence_visited)
