from simulation.node_generator import RandomNodeGenerator
from simulation.connection_generator import RandomGraphGenerator
from simulation.games import TwoPlayer
from simulation.agents import Agent, GroupAgent, IndividualAgent
import networkx as nx
import numpy as np

name = "degree"

NUM_GROUPS = 3
ITERATIONS = 1000

def test(csvwriter):
    Agent.reset()
    nodegen = RandomNodeGenerator([GroupAgent, IndividualAgent],
                                  NUM_GROUPS)
    conngen = RandomGraphGenerator(0.05)
    sim = TwoPlayer(100, nodegen, conngen)

    degrees = [sorted([d for n, d in sim.G.degree()])]

    for _ in range(ITERATIONS):
        actions = sim.play_game()
        sim.reproduce()
        sim.evolve_connections()

    degrees.append(sorted([d for n, d in sim.G.degree()]))

    csvwriter.writerows(np.transpose(degrees))
