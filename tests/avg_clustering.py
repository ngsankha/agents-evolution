from simulation.node_generator import RandomNodeGenerator
from simulation.connection_generator import RandomGraphGenerator
from simulation.games import TwoPlayer
from simulation.agents import Agent, GroupAgent, IndividualAgent
import networkx as nx
import numpy as np

name = "avg_clustering"

NUM_GROUPS = 20
ITERATIONS = 5000

def test(csvwriter):
    Agent.reset()
    nodegen = RandomNodeGenerator([GroupAgent, IndividualAgent],
                                  NUM_GROUPS)
    conngen = RandomGraphGenerator(0.05)
    sim = TwoPlayer(100, nodegen, conngen)

    csvwriter.writerow([nx.average_clustering(sim.G)])

    for i in range(ITERATIONS):
        actions = sim.play_game()
        sim.reproduce()
        sim.evolve_connections()

        if i % 500 == 0:
            csvwriter.writerow([nx.average_clustering(sim.G)])
