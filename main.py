# TODO: incorporate payoff in reproduction or edge formation
from node_generator import RandomNodeGenerator
from connection_generator import RandomGraphGenerator
from games import TwoPlayer
from agents import GroupAgent, IndividualAgent

NUM_GROUPS = 3
ITERATIONS = 10000

if __name__ == "__main__":
    nodegen = RandomNodeGenerator([GroupAgent, IndividualAgent],
                                  NUM_GROUPS)
    conngen = RandomGraphGenerator(0.05)
    n = TwoPlayer(100, nodegen, conngen)
    # n.show()

    group = 0
    ind = 0

    for node in n.G.nodes:
        if node.__class__.__name__ == 'GroupAgent':
            group += 1
        else:
            ind += 1
    print(group, ind)

    for _ in range(ITERATIONS):
        n.play_game()
        n.reproduce()
        # n.evolve_connections()

    group = 0
    ind = 0

    for node in n.G.nodes:
        if node.__class__.__name__ == 'GroupAgent':
            group += 1
        else:
            ind += 1
    print(group, ind)
    print("============")
