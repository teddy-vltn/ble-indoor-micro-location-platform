import pymongo
from pymongo import MongoClient
import sys
sys.path.append("./")
from lib.model import ModelNetwork
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation

# Connexion à MongoDB pour récupérer les données en temps réel
client = MongoClient('mongodb://192.168.2.1:27017/')
db = client['game_database']
players_collection = db['players']

m = ModelNetwork(file='data/scenario/model.gml')

fig, ax = plt.subplots(figsize=(10, 8))

def update(frame):
    ax.clear()

    players = players_collection.find({"has_finished": False})

    for player in players:

        minor = player["id_minor"]
        last_visited = player["last_visited"]        

        pos = nx.kamada_kawai_layout(m.graph)

        # Initialiser le dessin du graphe en arrière-plan
        nx.draw(m.graph, pos, with_labels=True, ax=ax)

        # Dessiner le joueur
        nx.draw_networkx_nodes(m.graph, pos, nodelist=[last_visited], node_color='r', ax=ax)

    return ax

ani = FuncAnimation(fig, update, interval=50)

plt.show()
