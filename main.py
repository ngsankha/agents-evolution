# TODO: There is no additional penalty for other groups
from simulation.node_generator import RandomNodeGenerator
from simulation.connection_generator import RandomGraphGenerator
from simulation.games import TwoPlayer
from simulation.agents import GroupAgent, IndividualAgent
import community
import networkx as nx

NUM_GROUPS = 10
ITERATIONS = 10000

if __name__ == "__main__":
    nodegen = RandomNodeGenerator([GroupAgent, IndividualAgent],
                                  NUM_GROUPS)
    conngen = RandomGraphGenerator(0.05)
    sim = TwoPlayer(100, nodegen, conngen)
    degree_sequence = sorted([d for n, d in sim.G.degree()], reverse=True)
    print(degree_sequence[:5])
    sim.show()

    for _ in range(ITERATIONS):
        sim.play_game()
        sim.reproduce()
        sim.evolve_connections()

        # print(len(max(nx.connected_components(sim.G), key=len)))
        # print(sorted([d for n, d in sim.G.degree()], reverse=True)[0:5])

    print("Simulation finished")
    degree_sequence = sorted([d for n, d in sim.G.degree()], reverse=True)
    print(degree_sequence[:5])
    sim.show()
