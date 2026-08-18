import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import lib.model as model
import lib.trajectory as trajectory
import lib.reader as reader
import sched, time

from bson import ObjectId

from modules.database.database import db, logs_collection, players_collection

from modules.database.query.get_active_profile_graph import get_active_profile_graph
from modules.database.query.get_active_profile_group import get_active_profile_group
from modules.database.query.get_active_session_players import get_active_session_players

from lib.util.load_config import load_config

# Load configuration from YAML file
config = load_config()

SCHEDULER_SETTINGS = config["scheduler_settings"]

def build_network_edges_from_db():
    # Model is edges collection and we can build a network from it
    graph = get_active_profile_graph()

    # We can build a network from this data
    model_edges = graph["edges"]

    # each edge is a dictionary with the following keys "from", "to"
    # "from" and "to" are the ids of the nodes
    # We can build a network from this data
    model_edges = list(model_edges)
    model_edges = [ (edge["from"], edge["to"]) for edge in model_edges ]
    # Transform to networkx format
    model_edges = [(str(edge[0]), str(edge[1])) for edge in model_edges]

    m = model.ModelNetwork(edges=model_edges)
    return m, model_edges

def build_raspberry_data_from_db():
    group = get_active_profile_group()

    raspberrys = group["hosts"]
    raspberrys = { raspberry["name"]: raspberry["node"] for raspberry in raspberrys }

    p = reader.RaspberryPiDataReader(collection=raspberrys)
    return p, raspberrys

def compute(scheduler):

    scheduler.enter(
        SCHEDULER_SETTINGS["interval"], 
        SCHEDULER_SETTINGS["priority"], 
        compute, (scheduler,))
    
    m, model_edges = build_network_edges_from_db()
    p, raspberrys = build_raspberry_data_from_db()

    print("""
    Loaded configuration:
        - Model file path: {}
        - Raspberry data file: {}
        - Scheduler settings: {}
        """.format(model_edges, raspberrys, SCHEDULER_SETTINGS))

    players = get_active_session_players()

    print("Checking players: ", players)

    if not players:
        return

    players_data = {}

    for player in players:
        if player.get("id_minor") is None:
            continue

        print("Processing player: ", player["id_minor"])
        players_data[player["id_minor"]] = {
            "_id": player["_id"],
            "id_minor": player["id_minor"],
            "updated_at": player["updated_at"],
            #"updated_at": "2024-03-27 16:41:20.639",
            "last_visited": player["last_visited"] if "last_visited" in player else None,
            "temporal_sequence_visited": player["temporal_sequence_visited"],
            "has_visited": player["has_visited"],
        }

    if len(players_data) == 0:
        return

    query_conditions = []
    for _, player_data in players_data.items():
        print("Processing player minor: ", player_data["id_minor"])
        condition = {
            "minor": player_data["id_minor"],
            "timestamp": {
                "$gte": player_data["updated_at"]
            }
        }
        query_conditions.append(condition)

    query = {"$or": query_conditions}

    print(query)

    logs = logs_collection.find(query).sort("timestamp", 1)

    print("Processing logs: ", logs)

    r = reader.BeaconDataReader(data=logs, rasp_data=p.data)

    for _, beacon_data in r.beacons_data.items():

        print("Processing beacon data for minor: ", beacon_data.minor)

        if len(beacon_data.data) < 50:
            print(len(beacon_data.data))
            print("Not enough data yet for minor: ", beacon_data.minor)
            continue

        minor = beacon_data.minor
        player_data = players_data[minor]
        last_visited = player_data["last_visited"]
        has_visited = player_data["has_visited"]

        player_path = trajectory.PlayerNetworkPath(beacon_data, m, has_visited, last_visited)
        player_path.load_settings(default_settings=True)
        player_trace = player_path.move_in_network()

        player_data["has_visited"] = player_trace.has_visited_beacons
        player_data["last_visited"] = player_trace.last_visited_beacon

        if player_trace.last_visited_beacon is not None:
            player_data["updated_at"] = player_trace.last_data_time or player_data["updated_at"]

        # Updating the temporal sequence of visited places
        if "temporal_sequence_visited" not in player_data:
            player_data["temporal_sequence_visited"] = {}
        
        player_data["temporal_sequence_visited"].update(player_trace.temporal_sequence_visited)

        # Remove the _id key from the player data
        player_id = player_data["_id"]
        player_data.pop("_id")

        # Update the player document in MongoDB
        players_collection.update_one({"_id": ObjectId(player_id)}, {"$set": player_data})

    return

scheduler = sched.scheduler(time.time, time.sleep)
scheduler.enter(1, 1, compute, (scheduler,))
scheduler.run()
