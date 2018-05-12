from simulation.node_generator import RandomNodeGenerator
from simulation.connection_generator import RandomGraphGenerator
from simulation.games import TwoPlayer
from simulation.agents import Agent, GroupAgent, IndividualAgent

name = "strategy_risk_taking"

NUM_GROUPS = 10
ITERATIONS = 10000

def test(csvwriter):
    Agent.reset()
    nodegen = RandomNodeGenerator([GroupAgent, IndividualAgent],
                                  NUM_GROUPS)
    conngen = RandomGraphGenerator(0.05)
    sim = TwoPlayer(100, nodegen, conngen)

    for _ in range(ITERATIONS):
        actions = sim.play_game()
        sim.reproduce()
        sim.evolve_connections()

        csvwriter.writerow(actions)
