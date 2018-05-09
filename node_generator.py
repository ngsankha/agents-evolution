import random


class RandomNodeGenerator:
    # kinds: an array of the classes Agent that would be generated
    # num_groups: number of groups to be formed
    def __init__(self, kinds, num_groups):
        self.kinds = kinds
        self.num_groups = num_groups

    def generate(self, graph):
        agent_type = random.choice(self.kinds)
        group = random.randint(0, self.num_groups - 1)
        agent = agent_type(graph, group)
        return agent
