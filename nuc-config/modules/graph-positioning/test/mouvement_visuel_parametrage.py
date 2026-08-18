import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, CheckButtons
from matplotlib.animation import FuncAnimation

import os
import sys

g_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

sys.path.append(g_path)

from lib.reader import BeaconDataReader
from lib.model import ModelNetwork
from lib.trajectory import PlayerNetworkPath
import networkx as nx
from lib.util.load_config import load_config

config = load_config()

dataset = config['test_dataset']

# Initialisation des données
r = BeaconDataReader(file=g_path + '/data/' + dataset + '/beacons.json')
m = ModelNetwork(file=g_path + '/data/' + dataset + '/model.gml')

rssi_max = r.rssi_max
rssi_min = r.rssi_min

# Prendre le premier beacon pour l'exemple
n = 0
beacon_data = list(r.beacons_data.values())[n]

def create_player_network_path(
        average_rssi_weight=0.80, 
        beacon_count_weight=0.25, 
        confidence_threshold_weight=0.5,
        distance_weight=0.248,
        min_distance=0.1,
        max_distance=3.5,
        min_rssi=-90,
        max_rssi=-75,
        time_interval_of_groups=8
    ):
    print("Processing beacon data for minor: ", beacon_data.minor)
    p = PlayerNetworkPath(
        beacon_data,
        m,)
    
    p.load_settings(
        time_interval_of_groups=time_interval_of_groups,
        definition={
            'AVERAGE_RSSI_WEIGHT': average_rssi_weight, 
            'BEACON_COUNT_WEIGHT': beacon_count_weight, 
            'CONFIDENCE_THRESHOLD': confidence_threshold_weight,
            'DISTANCE_WEIGHT': distance_weight, 
            'RSSI_MIN': min_rssi,
            'RSSI_MAX': max_rssi,
            'DISTANCE_MAX': max_distance,
            'DISTANCE_MIN': min_distance ,
        },
        debug=False 
    )

    r = p.move_in_network().temporal_sequence_visited
    return r

# Initialiser la séquence
sequence = create_player_network_path(0.5, 0.5)

fig, ax = plt.subplots(figsize=(13, 8))
plt.subplots_adjust(left=0.3, bottom=0.2)  # Ajustez pour laisser de la place aux Widgets

pos = nx.rescale_layout_dict(nx.kamada_kawai_layout(m.graph), 1.5)

# Affichage initial du graphe
nx.draw(m.graph, pos, with_labels=True, node_color='lightgrey', edge_color='grey', ax=ax)

# Slider pour ajuster AVERAGE_RSSI_WEIGHT
axSlider1 = plt.axes([0.15, 0.8, 0.1, 0.03], facecolor='lightgoldenrodyellow')
slider1 = Slider(axSlider1, 'AVERAGE_RSSI_WEIGHT', 0.0, 1.0, valinit=0.7)

# Slider pour ajuster BEACON_COUNT_WEIGHT
axSlider2 = plt.axes([0.15, 0.75, 0.1, 0.03], facecolor='lightgoldenrodyellow')
slider2 = Slider(axSlider2, 'BEACON_COUNT_WEIGHT', 0.0, 1.0, valinit=0.3)

# CONFIDENCE_THRESHOLD
axSlider4 = plt.axes([0.15, 0.7, 0.1, 0.03], facecolor='lightgoldenrodyellow')
slider4 = Slider(axSlider4, 'CONFIDENCE_THRESHOLD', 0.0, 1.0, valinit=0.45)

# DISTANCE_WEIGHT
axSlider5 = plt.axes([0.15, 0.65, 0.1, 0.03], facecolor='lightgoldenrodyellow')
slider5 = Slider(axSlider5, 'DISTANCE_WEIGHT', 0.0, 1.0, valinit=0.3)

# DISTANCE_MIN
axSlider6 = plt.axes([0.15, 0.6, 0.1, 0.03], facecolor='lightgoldenrodyellow')
slider6 = Slider(axSlider6, 'DISTANCE_MIN', -1, 1, valinit=-0.5)

# DISTANCE_MAX
axSlider7 = plt.axes([0.15, 0.55, 0.1, 0.03], facecolor='lightgoldenrodyellow')
slider7 = Slider(axSlider7, 'DISTANCE_MAX', 0, 10, valinit=3)

# RSSI_MIN
axSlider9 = plt.axes([0.15, 0.45, 0.1, 0.03], facecolor='lightgoldenrodyellow')
slider9 = Slider(axSlider9, 'RSSI_MIN', -100, 0, valinit=rssi_min)

# RSSI_MAX
axSlider10 = plt.axes([0.15, 0.4, 0.1, 0.03], facecolor='lightgoldenrodyellow')
slider10 = Slider(axSlider10, 'RSSI_MAX', -100, 0, valinit=rssi_max)

# TIME_INTERVAL_OF_GROUPS
axSlider8 = plt.axes([0.15, 0.5, 0.1, 0.03], facecolor='lightgoldenrodyellow')
slider8 = Slider(axSlider8, 'TIME_INTERVAL_OF_GROUPS', 0, 300, valinit=8)

# Slider pour naviguer dans les étapes du chemin
axSlider3 = plt.axes([0.1, 0.1, 0.8, 0.03], facecolor='lightgoldenrodyellow')
slider3 = Slider(axSlider3, 'Étape', 0, len(sequence), valinit=0, valstep=1)

axNextButton = plt.axes([0.8, 0.05, 0.1, 0.04])
nextButton = Button(axNextButton, 'Suivant', color='lightgoldenrodyellow', hovercolor='0.975')

axPreviousButton = plt.axes([0.7, 0.05, 0.1, 0.04])
previousButton = Button(axPreviousButton, 'Précédent', color='lightgoldenrodyellow', hovercolor='0.975')

lockStepCheckbox = CheckButtons(plt.axes([0.15, 0.15, 0.1, 0.05]), ['Lock step'], [False])
lockStep = False

def lock_step(label):
    global lockStep
    lockStep = not lockStep

lockStepCheckbox.on_clicked(lock_step)

def compute_graph():
    return create_player_network_path(slider1.val, slider2.val, slider4.val, slider5.val, slider6.val, slider7.val, slider9.val, slider10.val, slider8.val)

def next_step(event):
    global beacon_data, sequence, n, ax
    ax.clear()
    n += 1
    beacon_data = list(r.beacons_data.values())[n]
    sequence = compute_graph()
    recalculate(None)

nextButton.on_clicked(next_step)

def previous_step(event):
    global beacon_data, sequence, n, ax
    ax.clear()
    n -= 1
    beacon_data = list(r.beacons_data.values())[n]
    sequence = compute_graph()

    recalculate(None)

previousButton.on_clicked(previous_step)

# Bouton pour recalculer le chemin
axButton = plt.axes([0.15, 0.3, 0.1, 0.04])
button = Button(axButton, 'Recalculer', color='lightgoldenrodyellow', hovercolor='0.975')

def recalculate(event):
    global sequence, slider3
    sequence = compute_graph()

    slider3.valmax = len(sequence)

    if not lockStep:
        slider3.set_val(len(sequence)) 
    else:
        slider3.set_val(slider3.val)

    slider3.ax.set_xlim(0, len(sequence))

    update_graph(slider3.val) 

def update_graph(step):
    ax.clear()
    nx.draw(m.graph, pos, with_labels=True, node_color='lightgrey', edge_color='grey', ax=ax)

    current_passed_nodes = set()
    current_passed_edges = []

    already_passed_nodes = set()
    already_passed_edges = []

    new_passed_nodes = set()
    new_passed_edges = []

    date = None
    last_score = 0
    go_to = None
    from_node = None

    i = 0
    for key, value in sequence.items():
        if i < step:
            if value['from'] is not None:
                current_passed_nodes.add(str(value['from']))
                last_visited = value['from']
                for to_node in value['to']:
                    current_passed_edges.append((str(last_visited), str(to_node)))
                    current_passed_nodes.add(str(to_node))
                    last_visited = to_node
                last_score = value['score']
                go_to = value['to']
                from_node = value['from']
                date = key
        elif i == step:
            if value['from'] is not None:
                new_passed_nodes.add(str(value['from']))
                last_visited = value['from']
                for to_node in value['to']:
                    edge = (str(last_visited), str(to_node))
                    reversed_edge = (str(to_node), str(last_visited))
                    
                    if edge in current_passed_edges or reversed_edge in current_passed_edges:
                        new_passed_edges.append(edge)
                    else:
                        already_passed_edges.append(edge)

                    if str(to_node) in current_passed_nodes:
                        new_passed_nodes.add(str(to_node))
                    else:
                        already_passed_nodes.add(str(to_node))

                    last_visited = to_node
                last_score = value['score']
                go_to = value['to']
                from_node = value['from']
                date = key
        i += 1

    # draw text score and go to
    ax.text(1, 1.1, f"Score: {last_score}", horizontalalignment='right', verticalalignment='top', transform=ax.transAxes)
    ax.text(1, 0.15, f"Go to: {go_to}", horizontalalignment='right', verticalalignment='top', transform=ax.transAxes)
    ax.text(1, 0.20, f"From: {from_node}", horizontalalignment='right', verticalalignment='top', transform=ax.transAxes)
    ax.text(-0.1, 0.1, f"Date: {date}", horizontalalignment='left', verticalalignment='top', transform=ax.transAxes)

    current_passed_nodes = {node for node in current_passed_nodes}
    current_passed_edges = [(edge[0], edge[1]) for edge in current_passed_edges]

    new_passed_nodes = {node for node in new_passed_nodes}
    new_passed_edges = [(edge[0], edge[1]) for edge in new_passed_edges]

    # Dessiner les nœuds et arêtes parcourus jusqu'à l'étape courante
    nx.draw_networkx_nodes(m.graph, pos, nodelist=current_passed_nodes, node_color='b', node_size=500, ax=ax)
    nx.draw_networkx_edges(m.graph, pos, edgelist=current_passed_edges, edge_color='b', width=2, ax=ax)

    # Dessiner les nœuds et arêtes déjà parcourus
    nx.draw_networkx_nodes(m.graph, pos, nodelist=already_passed_nodes, node_color='g', node_size=500, ax=ax)
    nx.draw_networkx_edges(m.graph, pos, edgelist=already_passed_edges, edge_color='g', width=2, ax=ax)

    # Dessiner les nouveaux nœuds et arêtes parcourus à l'étape courante
    nx.draw_networkx_nodes(m.graph, pos, nodelist=new_passed_nodes, node_color='r', node_size=500, ax=ax)
    nx.draw_networkx_edges(m.graph, pos, edgelist=new_passed_edges, edge_color='r', width=2, ax=ax)

button.on_clicked(recalculate)

def update_slider(val):
    update_graph(int(val))

slider3.on_changed(update_slider)
slider3.set_val(0)

recalculate(None)  # Afficher le graphe initial

plt.show()
