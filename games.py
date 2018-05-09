import networkx as nx
import matplotlib.pyplot as plt
from math import exp
import random
from globals import DEFECT, COOPERATE, DEFECT_DEFECT, COOPERATE_DEFECT, \
                    DEFECT_COOPERATE, COOPERATE_COOPERATE, S


class TwoPlayer:
    def __init__(self, num_nodes, nodegen, conngen):
        self.G = nx.Graph()
        for _ in range(num_nodes):
            node = nodegen.generate(self.G)
            self.G.add_node(node)
        conngen.generate(self.G)

    # show the state of the network
    def show(self):
        nx.draw(self.G, cmap=plt.get_cmap('jet'))
        plt.show()

    def reproduce(self):
        min_payoff = min([node.payoff for node in self.G])
        max_payoff = max([node.payoff for node in self.G])
        range_payoff = max_payoff - min_payoff

        # get a list of nodes because we'll change the iterator
        orig_nodes = list(self.G.nodes)

        for node in orig_nodes:
            neighbors = list(self.G.neighbors(node))
            neighbors = list(filter(lambda n: n.payoff > node.payoff,
                                    neighbors))
            if len(neighbors) == 0:
                continue
            teacher = random.choice(neighbors)
            teacher_payoff = (teacher.payoff - min_payoff) / range_payoff
            node_payoff = (node.payoff - min_payoff) / range_payoff
            diff = teacher_payoff - node_payoff

            # NOTE: we don't see increase in GroupAgents because we are not
            # favoring the GroupAgents in any way
            if random.random() < 1 / (1.0 + exp(S * diff)):
                # replacing the node takes all this work
                new_node = teacher.__class__(self.G, node.group)
                # print(node.__class__.__name__, new_node.__class__.__name__)
                # replicate the memory
                # new_node.memory = teacher.memory
                self.G.add_node(new_node)
                for n in neighbors:
                    self.G.add_edge(new_node, n)
                self.G.remove_node(node)

    def play_game(self):
        # reset all state variables for this round
        for node in self.G:
            node.reset()

        # play the round
        for node in self.G:
            neighbors = self.G.neighbors(node)
            for neighbor in neighbors:
                # skip if this node has had it's turn this round
                if node in neighbor.played:
                    continue
                p1_action = node.move(neighbor)
                p2_action = neighbor.move(node)

                if p1_action == DEFECT and p2_action == DEFECT:
                    node.payoff += DEFECT_DEFECT[0]
                    neighbor.payoff += DEFECT_DEFECT[1]
                elif p1_action == COOPERATE and p2_action == COOPERATE:
                    node.payoff += COOPERATE_COOPERATE[0]
                    neighbor.payoff += COOPERATE_COOPERATE[1]
                elif p1_action == DEFECT and p2_action == COOPERATE:
                    node.payoff += DEFECT_COOPERATE[0]
                    neighbor.payoff += DEFECT_COOPERATE[1]
                else:
                    node.payoff += COOPERATE_DEFECT[0]
                    neighbor.payoff += COOPERATE_DEFECT[1]

                node.played.add(neighbor)
                neighbor.played.add(node)

                node.add_to_memory(neighbor, p2_action)
                neighbor.add_to_memory(node, p1_action)

        # round is over, reproduce, clean-up and set the stage for next
        for node in self.G:
            node.commit_memory()
            # TODO: sever ties and make new ones based on payoff
