COOPERATE = 0
DEFECT = 1

IN_P = 1
IN_Q = 1
IN_I = 1
OUT_P = 1
OUT_Q = 1
OUT_I = 1
IND_P = 1
IND_Q = 1
IND_I = 1


class Agent:
    __i = 0

    def __init__(self, features):
        self.i = Agent.__i
        Agent.__i += 1

        self.memory = {}
        self.features = features


class GroupAgent(Agent):
    def __init__(self, features=None):
        Agent.__init__(self, features)

    def move(self, p2):
        p1_tag = self.features['group']
        p2_tag = p2.features['group']

        # check if p2 defected against any neighbor that are in my group
        group_neighbors = [n for n in self.G.neighbors(self)
                           if n.features['group'] == p1_tag]
        for n in group_neighbors:
            if p2_tag in n.memory.keys() and \
               n.memory[p2_tag] == DEFECT:
                if p1_tag == p2_tag:
                    return IN_Q
                else:
                    return OUT_Q

        # check if self encountered p2's group before
        if p2_tag in self.memory.keys():
            if self.memory[p2_tag] == COOPERATE:
                if p1_tag == p2_tag:
                    return IN_P
                else:
                    return OUT_P
            else:
                if p1_tag == p2_tag:
                    return IN_Q
                else:
                    return OUT_Q


class IndividualAgent(Agent):
    def __init__(self, features=None):
        Agent.__init__(self, features)

    def move(self, p2):
        if p2 in self.memory.keys():
            if self.memory[p2] == COOPERATE:
                return IND_P
            else:
                return IND_Q
        else:
            return IND_I
