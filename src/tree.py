from node import Node


class Tree(object):

    AND = 0
    OR = 1
    PLACE = 2

    def __init__(self, classification: int, node: Node=None, size: int=0):
        self.classification = classification  # type: int
        self.next = [None] * size  # type: List[Tree]
        self.node = node  # type: Node

    def __str__(self):
        if self.classification == self.AND:
            name = "AND"
        elif self.classification == self.OR:
            name = "OR"
        else:
            name = self.node.name
        return name + " " + str(self.next)

    def __repr__(self):
        if self.classification == self.AND:
            name = "AND"
        elif self.classification == self.OR:
            name = "OR"
        else:
            name = self.node.name
        return name + " " + str(self.next)