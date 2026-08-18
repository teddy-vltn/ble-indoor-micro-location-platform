import sys
sys.path.append("./")
from lib.model import ModelNetwork

import matplotlib.pyplot as plt

import networkx as nx

m = ModelNetwork(file='data/scenario/model.gml')

pos = nx.kamada_kawai_layout(m.graph)

ax = plt.gca()

nx.draw(m.graph, pos, with_labels=True, node_color='lightgrey', edge_color='grey', ax=ax)

plt.show()

