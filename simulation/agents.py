import random
from globals import DEFECT, COOPERATE, MEMORY_SIZE, TRACK_INDIVIDUAL, RISK_AVERSE


class Agent:
    __i = 0

    def __init__(self, graph, group):
        self.i = Agent.__i
        Agent.__i += 1

        self.played = set()
        self.group = group
        self.payoff = 0
        self.G = graph

    def reset():
        Agent.__i = 0

    def calc_move(self, prob):
        p = random.random()
        if p < prob:
            return DEFECT
        else:
            return COOPERATE


class GroupAgent(Agent):
    def __init__(self, graph, group):
        Agent.__init__(self, graph, group)
        self.memory = {}
        self.temp_memory = {}

    def reset(self):
        self.temp_memory = {}
        self.played = set()
        self.payoff = 0

    def add_to_memory(self, other, move):
        if other.group in self.temp_memory:
            self.temp_memory[other.group].append(move)
        else:
            self.temp_memory[other.group] = [move]

    def commit_memory(self):
        for group, moves in self.temp_memory.items():
            if group in self.memory:
                self.memory[group].extend(moves)
                if len(self.memory[group]) > MEMORY_SIZE:
                    self.memory[group] = self.memory[group][(len(
                        self.memory[group]) - MEMORY_SIZE):]
            else:
                self.memory[group] = moves

    # returns the weighted average of memory as a chance of defection
    def defect_probability(self, other):
        if other.group in self.memory:
            memory_length = len(self.memory[other.group])
            defects = 0
            total = 0
            for i in range(memory_length):
                weight = i + 1
                defects += weight * self.memory[other.group][i]
                total += weight
            for i in range(len(self.memory[other.group]), MEMORY_SIZE):
                weight = i + 1
                defects += weight * 0.5
                total += weight
            defect_prob = defects / float(total)
            return defect_prob
        else:
            # if never played before, equal chance of defect
            return 0.5

    def move(self, p2):
        p1_group = self.group

        # check if p2 defected against any me or neighbor that are in my group
        group_neighbors = [n for n in self.G.neighbors(self)
                           if n.group == p1_group]
        group_neighbors.append(self)

        if RISK_AVERSE:
            risk = max
        else:
            risk = min

        defect_prob = risk(map(lambda n: n.defect_probability(p2),
                          group_neighbors))
        return self.calc_move(defect_prob)


class IndividualAgent(Agent):
    def __init__(self, graph, group):
        Agent.__init__(self, graph, group)
        if TRACK_INDIVIDUAL:
            self.memory = {}
            self.temp_memory = {}
        else:
            self.memory = []
            self.temp_memory = []

    def reset(self):
        if TRACK_INDIVIDUAL:
            self.temp_memory = {}
        else:
            self.temp_memory = []
        self.played = set()
        self.payoff = 0

    def add_to_memory(self, other, move):
        if TRACK_INDIVIDUAL:
            if other.i in self.temp_memory:
                self.temp_memory[other.i].append(move)
            else:
                self.temp_memory[other.i] = [move]
        else:
            self.temp_memory.append(move)

    def commit_memory(self):
        if TRACK_INDIVIDUAL:
            for i, moves in self.temp_memory.items():
                if i in self.memory:
                    self.memory[i].extend(moves)
                    if len(self.memory[i]) > MEMORY_SIZE:
                        self.memory[i] = self.memory[i][(len(
                            self.memory[i]) - MEMORY_SIZE):]
                else:
                    self.memory[i] = moves
        else:
            self.memory.extend(self.temp_memory)
            if len(self.memory) > MEMORY_SIZE:
                self.memory = self.memory[(len(self.memory) - MEMORY_SIZE):]

    # returns the weighted average of memory as a chance of defection
    def defect_probability(self, other):
        if TRACK_INDIVIDUAL:
            if other.i in self.memory:
                memory = self.memory[other.i]
            else:
                memory = []
        else:
            memory = self.memory

        if len(memory) == 0:
            return 0.5

        defects = 0
        total = 0
        for i in range(len(memory)):
            weight = i + 1
            defects += weight * memory[i]
            total += weight
        for i in range(len(memory), MEMORY_SIZE):
            weight = i + 1
            defects += weight * 0.5
            total += weight
        defect_prob = defects / float(total)
        return defect_prob

    def move(self, p2):
        defect_prob = self.defect_probability(p2)
        return self.calc_move(defect_prob)
