import random


class RandomGraphGenerator:
    def __init__(self, p):
        self.p = p

    def generate(self, G):
        nodes = list(G)
        n = len(nodes)
        for x in range(n):
            for y in range(x, n):
                if (random.random() < self.p or self.p == 1.0) and (x != y):
                    G.add_edge(nodes[x], nodes[y])
