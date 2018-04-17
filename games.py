class TwoPlayer:
    def __init__(self, G):
        self.G = G

    def play(self):
        nodes = self.G.nodes
        for node in nodes:
            neighbors = self.G.neighbors(node)
            for neighbor in neighbors:
                payoff = node.move(neighbor)
                print(payoff)
                node.payoff = payoff
