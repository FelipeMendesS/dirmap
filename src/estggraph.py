import re
from typing import List, Dict, Tuple, Union, Set
from textparseestg import TextParseESTG
from node import Node
Transition = List[Tuple[str, int]]


class ESTGGraph (object):
    '''
    Class that stores ESTG graph.
    '''
    # Data that we need to use
    # Check if we can have a choice to different concurrency, at first won't be implemented. Can change data structures
    # if needed.

    # Signals classifications
    INPUT = 0
    OUTPUT = 1
    CONDITIONAL_SIGNAL = 2

    SYMBOL_DICT = {
        Node.RISING_EDGE: ["", "+"],
        Node.FALLING_EDGE: ["", "-"],
        Node.DONT_CARE: ["", "*"],
        Node.LEVEL_HIGH: ["[", "+]"],
        Node.LEVEL_LOW: ["[", "-]"]
    }

    def __init__(self, text_parse: TextParseESTG):
        # Map to relate all variables to type (Input, output, conditional signal)
        self.signal_map = {}  # type: Dict[str, int]
        # Map that shows places graph
        self.stg_graph = {}  # type: Dict[Node, Set[Node]]
        # Map that shows the variables involved in each and every transition in the graph. The keys are made by the
        # concatenation of the nodes names
        self.stg_graph_transitions = {}  # type: Dict[Tuple[Node, Node], Node]
        # Map that stores the real complete graph, considering also the transitions as nodes.
        self.extended_graph = {}  # type: Dict[Node, List[Node]]
        # Same map but inverted
        self.inverted_extended_graph = {}  # type: Dict[Node, List[Node]]
        # List of places starting with tokens
        self.initial_places = text_parse.initial_places  # type: List[Node]
        # Map of signals and their initial values
        self.initial_signal_values = text_parse.initial_signal_values  # type: Dict[str, Union[int,str]]
        transition_count = 0
        for regular_input in text_parse.regular_inputs:
            self.signal_map[regular_input] = self.INPUT
        for output in text_parse.outputs:
            self.signal_map[output] = self.OUTPUT
        for conditional_signal in text_parse.conditional_signals:
            self.signal_map[conditional_signal] = self.CONDITIONAL_SIGNAL
        place_objects = {}  # type: Dict[str, Node]
        for node in self.initial_places:
            place_objects[node.name] = node
        for line in text_parse.transitions:
            [vertices, variables] = map(str.strip, line.split('|'))
            transition = Node(False, transition_count=transition_count, transition_text=variables)
            transition_count += 1
            [origin_vertex, destination_vertex] = map(str.strip, vertices.split('/'))
            self.inverted_extended_graph[transition] = []
            for origin in map(str.strip, origin_vertex.split(',')):
                if origin in place_objects:
                    origin_node = place_objects[origin]
                else:
                    origin_node = Node(True, name=origin)
                    place_objects[origin] = origin_node
                if origin_node not in self.stg_graph:
                    self.stg_graph[origin_node] = set()
                if origin_node not in self.extended_graph:
                    self.extended_graph[origin_node] = [transition]
                elif transition not in self.extended_graph[origin_node]:
                    self.extended_graph[origin_node].append(transition)
                if origin_node not in self.inverted_extended_graph[transition]:
                    self.inverted_extended_graph[transition].append(origin_node)
                self.extended_graph[transition] = []
                for destination in destination_vertex.split(','):
                    if destination in place_objects:
                        destination_node = place_objects[destination]
                    else:
                        destination_node = Node(True, name=destination)
                        place_objects[destination] = destination_node
                    self.stg_graph[origin_node].add(destination_node)
                    self.stg_graph_transitions[(origin_node, destination_node)] = transition
                    self.extended_graph[transition].append(destination_node)
                    if destination_node not in self.inverted_extended_graph:
                        self.inverted_extended_graph[destination_node] = [transition]
                    elif transition not in self.inverted_extended_graph[destination_node]:
                        self.inverted_extended_graph[destination_node].append(transition)
        self.__classify_nodes()
        self.__check_variables_use()

    def check_consistency(self):
        # TODO: Make this more efficient
        # TODO: Known Issue! In case of concurrency the results are not exactly the expected yet.
        order_of_signal_list = []
        signal_list = list(self.signal_map.keys())
        for signal in signal_list:
            if self.signal_map[signal] != self.CONDITIONAL_SIGNAL:
                order_of_signal_list.append(signal)
        current_signal_values = self.initial_signal_values
        current_place = self.initial_places
        visited_graph_map = {}
        for place in current_place:
            visited_graph_map[place] = self.get_current_signal_values(current_signal_values, order_of_signal_list)
            self.aux_check_consistency(visited_graph_map, current_signal_values, place, order_of_signal_list)
        # print("STG is consistent")

    # Will redo completey algorithm
    def aux_check_consistency(self, visited_graph_map, current_signal_values, current_place, order_of_signal_list):
        for destination in self.stg_graph[current_place]:
            signal_values = dict(current_signal_values)  # Just copying
            for signal, transition_type in self.stg_graph_transitions[(current_place, destination)].transition:
                if transition_type == Node.RISING_EDGE:
                    if signal_values[signal] == 0 or signal_values[signal] == "*":
                        signal_values[signal] = 1
                    else:
                        raise Exception("Inconsistent transition between place " + current_place + " and place " +
                                        destination.name + ". " + signal +
                                        " was 1 and is expected to rise in this transition")
                elif transition_type == Node.FALLING_EDGE:
                    if signal_values[signal] == 1 or signal_values[signal] == "*":
                        signal_values[signal] = 0
                    else:
                        raise Exception("Inconsistent transition between place " + current_place.name + " and place " +
                                        destination.name + ". " + signal +
                                        " was 0 and is expected to fall in this transition")
            if destination not in visited_graph_map:
                visited_graph_map[destination] = self.get_current_signal_values(signal_values, order_of_signal_list)
                self.aux_check_consistency(visited_graph_map, signal_values, destination, order_of_signal_list)
            elif self.get_current_signal_values(signal_values, order_of_signal_list) != visited_graph_map[destination]:
                # Add which signal is different between them to make it easier to identify which
                raise Exception("Inconsistent path coming and going to place" + destination.name)

    def check_output_persistency(self):
        for node in self.stg_graph:
            if node.is_choice_open():
                for transition in self.extended_graph[node]:
                    if transition.contains_type(self.signal_map, Node.OUTPUT):
                        raise Exception("In the decision coming from place " + node.name +
                                        ", one of the transitions contain an output signal. "
                                        "Thus this ESTG is not output persistent.")
        # print("ESTG is output-persistent!")
        return

    def __check_variables_use(self):
        variable_check_map = dict.fromkeys(self.signal_map.keys(), 0)
        for transition in self.stg_graph_transitions.values():
            for variable, transition_type in transition.transition:
                if variable in variable_check_map:
                    variable_check_map[variable] = 1
                else:
                    raise Exception("Variable not declared: " + variable)
        for key, transition in variable_check_map.items():
            if transition != 1:
                print("Warning! Variable", key, "declared but not used.")

    def __classify_nodes(self):
        for node in self.extended_graph.keys():
            length = len(self.extended_graph[node])
            if length > 1:
                if node.is_place:
                    node.classify = (Node.CHOICE_OPEN, [length])
                else:
                    node.classify = (Node.CONCURRENCY_OPEN, [length])
        for node in self.inverted_extended_graph.keys():
            length = len(self.inverted_extended_graph[node])
            if length > 1:
                if node.is_place:
                    if node.classify:
                        node.classify[1].append(length)
                        node.classify = (Node.CHOICE_CLOSE_OR_HUB, node.classify[1])
                    else:
                        node.classify = (Node.CHOICE_CLOSE_OR_HUB, [length])
                else:

                    if node.classify:
                        node.classify[1].append(length)
                        node.classify = (Node.CHOICE_CLOSE_OR_HUB, node.classify[1])
                    else:
                        node.classify = (Node.CONCURRENCY_CLOSE_OR_HUB, [length])

    @staticmethod
    def get_current_signal_values(current_signal_values, order_of_signal_list):
        signal_values = ""
        for signal in order_of_signal_list:
            signal_values += str(current_signal_values[signal])
        return signal_values
