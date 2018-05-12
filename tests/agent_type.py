from simulation.node_generator import RandomNodeGenerator
from simulation.connection_generator import RandomGraphGenerator
from simulation.games import TwoPlayer
from simulation.agents import Agent, GroupAgent, IndividualAgent

name = "agent_type"

NUM_GROUPS = 3
ITERATIONS = 1000

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
        group_count = 0
        ind_count = 0
        for n in sim.G:
            if n.__class__ == GroupAgent:
                group_count += 1
            elif n.__class__ == IndividualAgent:
                ind_count += 1
            else:
                raise "Error!"
        csvwriter.writerow([group_count, ind_count])
    print(set(map(lambda n: n.__class__.__name__, sim.G.nodes)))
