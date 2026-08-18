import networkx as nx

class ModelNetwork:
    def __init__(self, edges=None, file=None):

        self.graph = nx.Graph()
        self.nodes = []
        self.edges = []
        self.node_count = 0
        self.edge_count = 0

        if edges is not None:
            self.load_from_edges(edges)
        elif file is not None:
            self.load_from_file(file)
        else:
            raise Exception("No edges or file provided")

    def load_from_edges(self, edges):
        self.graph = nx.Graph()
        self.graph.add_edges_from(edges)
        self.nodes = self.graph.nodes()
        self.edges = self.graph.edges()
        self.node_count = len(self.nodes)
        self.edge_count = len(self.edges)

    def load_from_file(self, file):
        self.graph = nx.read_gml(file)
        self.nodes = self.graph.nodes()
        self.edges = self.graph.edges()
        self.node_count = len(self.nodes)
        self.edge_count = len(self.edges)

    def read_gml(self, file):
        try:
            self.graph = nx.read_gml(file)
        except Exception as e:
            print("Error reading GML file: ", e)
            return False
