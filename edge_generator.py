import random


def max_random(per_edge):
    def fn(g):
        if per_edge == 0:
            return

        nodes = g.nodes
        for n in nodes:
            selected = [n]
            while n in selected:
                selected = random.sample(nodes, per_edge)
            for other in selected:
                g.add_edge(n, other)
    return fn
