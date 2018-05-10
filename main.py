# TODO: There is no additional penalty for other groups
from node_generator import RandomNodeGenerator
from connection_generator import RandomGraphGenerator
from games import TwoPlayer
from agents import GroupAgent, IndividualAgent
import community
import networkx as nx

NUM_GROUPS = 10
ITERATIONS = 10000

if __name__ == "__main__":
    nodegen = RandomNodeGenerator([GroupAgent, IndividualAgent],
                                  NUM_GROUPS)
    conngen = RandomGraphGenerator(0.05)
    sim = TwoPlayer(100, nodegen, conngen)
    sim.show()

    for _ in range(ITERATIONS):
        sim.play_game()
        sim.reproduce()
        sim.evolve_connections()

        # print(len(max(nx.connected_components(sim.G), key=len)))
        # print(sorted([d for n, d in sim.G.degree()], reverse=True)[0:5])

    sim.show()
