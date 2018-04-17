import networkx as nx
import matplotlib.pyplot as plt


class Network:
    def __init__(self, num_nodes, node_generator):
        self.G = nx.Graph()
        for _ in range(num_nodes):
            node = node_generator()
            node.G = self.G
            self.G.add_node(node)

    def initial_connections(self, scheme):
        scheme(self.G)

    def show(self):
        nx.draw(self.G, cmap=plt.get_cmap('jet'))
        plt.show()

    def play_game(self):
        self.game.play()
