from typing import List, Dict, Tuple, Union, Set
import re
from functools import total_ordering


@total_ordering
class Node(object):
    '''
    Class to represent any node of a ESTG or STG graph.
    The idea is that it contains a place or a transition so we can add metadata, ordering and easy detection in order
    to make the code cleaner and easier to scale.
    The idea is for this to be immutable but I couldn't easily find the best way to do this in python.
    '''

    INPUT = 0
    OUTPUT = 1
    CONDITIONAL_SIGNAL = 2
    TRANSITION_NAME = "transition"
    # Transitions classifications
    RISING_EDGE = 3
    FALLING_EDGE = 4
    DONT_CARE = 5
    LEVEL_HIGH = 6
    LEVEL_LOW = 7
    # Node classifications
    CONCURRENCY_OPEN = 8
    CHOICE_OPEN = 9
    CONCURRENCY_CLOSE_OR_HUB = 10
    CHOICE_CLOSE_OR_HUB = 11

    def __init__(self, is_place: bool, name: str="", transition_count: int=0, transition_text: str=""):
        self.name = name  # type: str
        self.is_place = is_place  # type: str
        self.transition = []  # type: List[Tuple[str, int]]
        self.classify = ()  # type: Tuple[int, List[int]]
        if not self.is_place:
            self.name = self.TRANSITION_NAME + str(transition_count)
            for variable in map(str.strip, transition_text.split(',')):
                if re.match(r"#\w+[+\-*]", variable):
                    if variable[-1] == "+":
                        t = self.LEVEL_HIGH
                    elif variable[-1] == "-":
                        t = self.LEVEL_LOW
                    else:
                        t = self.DONT_CARE
                else:
                    if variable[-1] == "+":
                        t = self.RISING_EDGE
                    elif variable[-1] == "-":
                        t = self.FALLING_EDGE
                    else:
                        t = self.DONT_CARE
                v = variable.strip('#+-*')
                self.transition.append((v, t))

    def is_node_place(self):
        return self.is_place

    def is_choice_open(self):
        if self.classify:
            return self.classify[0] == self.CHOICE_OPEN or (self.classify[0] == self.CHOICE_CLOSE_OR_HUB and
                                                        len(self.classify)[1] == 2)
        return False

    def is_concurrency_open(self):
        if self.classify:
            return self.classify[0] == self.CONCURRENCY_OPEN or (self.classify[0] == self.CONCURRENCY_CLOSE_OR_HUB and
                                                             len(self.classify)[1] == 2)
        return False

    # Transition Functions

    def contains_type(self, signal_map, type_to_check):
        if self.is_place:
            return False
        else:
            for signal, transition in self.transition:
                if signal_map[signal] == type_to_check:
                    return True
            return False

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return False

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            if self.is_place != other.is_place:
                return self.is_place
            else:
                return self.name < other.name
        return False

    def __hash__(self):
        return hash(self.name + str(self.is_place) + str(self.transition))
