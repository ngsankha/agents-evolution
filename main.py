from network import Network
from node_generator import random_population
from edge_generator import max_random
from games import TwoPlayer
from agents import GroupAgent, IndividualAgent

if __name__ == "__main__":
    n = Network(100, random_population([GroupAgent, IndividualAgent]))
    n.initial_connections(max_random(2))
    n.game = TwoPlayer(n.G)
    # n.show()

    for _ in range(1000):
        n.play_game()
        # n.update_strategy()

    for node in n.G.nodes:
        print(node.payoff)
