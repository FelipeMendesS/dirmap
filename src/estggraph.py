import re
from typing import List, Dict, Tuple, Union, Set
from textparseestg import TextParseESTG
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

    SYMBOL_DICT = {
        3: ["", "+"],
        4: ["", "-"],
        5: ["", "*"],
        6: ["[", "+]"],
        7: ["[", "-]"]
    }

    def __init__(self, text_parse: TextParseESTG):
        # Map to relate all variables to type (Input, output, conditional signal)
        self.signal_map = {}  # type: Dict[str, int]
        # Map that shows places graph
        self.stg_graph = {}  # type: Dict[str, Set[str]]
        # Map that shows the variables involved in each and every transition in the graph. The keys are made by the
        # concatenation of the nodes names
        self.stg_graph_transitions = {}  # type: Dict[str, Transition]
        # Map that holds the identification of all transitions
        self.transitions_name_to_signal = {}  # type: Dict[str, Transition]
        # Map that stores the real complete graph, considering also the transitions as nodes.
        self.extended_graph = {}  # type: Dict[str, List[str]]
        # Same map but inverted
        self.inverted_extended_graph = {}  # type: Dict[str, List[str]]  Not sure If working, but assuming it is.
        # List of places starting with tokens
        self.initial_places = text_parse.initial_places  # type: List[str]
        # Map of signals and their initial values
        self.initial_signal_values = text_parse.initial_signal_values  # type: Dict[str, Union[int,str]]
        # Node classification to check concurrency and decisions
        self.node_classification = {}  # type: Dict[str,Tuple[int, List[int]]]
        transition_count = 0
        for regular_input in text_parse.regular_inputs:
            self.signal_map[regular_input] = self.INPUT
        for output in text_parse.outputs:
            self.signal_map[output] = self.OUTPUT
        for conditional_signal in text_parse.conditional_signals:
            self.signal_map[conditional_signal] = self.CONDITIONAL_SIGNAL
        for line in text_parse.transitions:
            [vertices, variables] = map(str.strip, line.split('|'))
            transition_conditions = []
            for variable in map(str.strip, variables.split(',')):
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
                transition_conditions.append((v, t))
            transition_count += 1
            transition_name = "transition" + str(transition_count)
            self.transitions_name_to_signal[transition_name] = transition_conditions
            [origin_vertex, destination_vertex] = map(str.strip, vertices.split('/'))
            self.inverted_extended_graph[transition_name] = []
            for origin in map(str.strip, origin_vertex.split(',')):
                if origin not in self.stg_graph:
                    self.stg_graph[origin] = set()
                if origin not in self.extended_graph:
                    self.extended_graph[origin] = [transition_name]
                else:
                    self.extended_graph[origin].append(transition_name)
                self.inverted_extended_graph[transition_name].append(origin)
                self.extended_graph[transition_name] = []
                for destination in destination_vertex.split(','):
                    self.stg_graph[origin].add(destination)
                    self.stg_graph_transitions[origin + destination] = transition_conditions
                    self.extended_graph[transition_name].append(destination)
                    if destination not in self.inverted_extended_graph:
                        self.inverted_extended_graph[destination] = [transition_name]
                    else:
                        self.inverted_extended_graph[destination].append(transition_name)
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
        print("STG is consistent")

    def aux_check_consistency(self, visited_graph_map, current_signal_values, current_place, order_of_signal_list):
        for destination in self.stg_graph[current_place]:
            signal_values = dict(current_signal_values)  # Just copying
            for signal, transition_type in self.stg_graph_transitions[current_place + destination]:
                if transition_type == self.RISING_EDGE:
                    if signal_values[signal] == 0 or signal_values[signal] == "*":
                        signal_values[signal] = 1
                    else:
                        raise Exception("Inconsistent transition between place " + current_place + " and place " +
                                        destination + ". " + signal +
                                        " was 1 and is expected to rise in this transition")
                elif transition_type == self.FALLING_EDGE:
                    if signal_values[signal] == 1 or signal_values[signal] == "*":
                        signal_values[signal] = 0
                    else:
                        raise Exception("Inconsistent transition between place " + current_place + " and place " +
                                        destination + ". " + signal +
                                        " was 0 and is expected to fall in this transition")
            if destination not in visited_graph_map:
                visited_graph_map[destination] = self.get_current_signal_values(signal_values, order_of_signal_list)
                self.aux_check_consistency(visited_graph_map, signal_values, destination, order_of_signal_list)
            elif self.get_current_signal_values(signal_values, order_of_signal_list) != visited_graph_map[destination]:
                # Add which signal is different between them to make it easier to identify which
                raise Exception("Inconsistent path coming and going to place" + destination)

    def check_concurrecy_consistency(self):
        return

    def check_output_persistency(self):
        for node in self.node_classification.keys():
            if node in self.stg_graph:
                for transition in self.extended_graph[node]:
                    for signal, transition_type in self.transitions_name_to_signal[transition]:
                        if self.signal_map[signal] == self.OUTPUT:
                            raise Exception("In the decision coming from place " + node +
                                            ", one of the transitions contain the output signal " + signal +
                                            ". Thus this ESTG is not output persistent.")
        print("ESTG is output-persistent!")
        return

    def __check_variables_use(self):
        variable_check_map = dict.fromkeys(self.signal_map.keys(), 0)
        for value in self.stg_graph_transitions.values():
            for variable, transition_type in value:
                if variable in variable_check_map:
                    variable_check_map[variable] = 1
                else:
                    raise Exception("Variable not declared: " + variable)
        for key, value in variable_check_map.items():
            if value != 1:
                print("Warning! Variable", key, "declared but not used.")

    def __classify_nodes(self):
        transition_fanin_count = {}
        for node in self.extended_graph.keys():
            if ESTGGraph.__is_place(node):
                if len(self.extended_graph[node]) > 1:
                    self.node_classification[node] = (ESTGGraph.CHOICE_OPEN, [len(self.extended_graph[node])])
                for transition in self.extended_graph[node]:
                    if transition not in transition_fanin_count:
                        transition_fanin_count[transition] = 1
                    else:
                        transition_fanin_count[transition] += 1
            else:
                if len(self.extended_graph[node]) > 1:
                    self.node_classification[node] = (ESTGGraph.CONCURRENCY_OPEN, [len(self.extended_graph[node])])
        for transition in transition_fanin_count:
            if transition_fanin_count[transition] > 1 and transition not in self.node_classification:
                self.node_classification[transition] = (ESTGGraph.CONCURRENCY_CLOSE_OR_HUB,
                                                        [transition_fanin_count[transition]])
            elif transition_fanin_count[transition] > 1:
                aux = self.node_classification[transition][1]
                aux.append(transition_fanin_count[transition])
                self.node_classification[transition] = (ESTGGraph.CONCURRENCY_CLOSE_OR_HUB, aux)
        for place in self.stg_graph.keys():
            aux = len(self.inverted_extended_graph[place])
            if aux > 1:
                if place in self.node_classification:
                    choice_open_index = self.node_classification[place][1]
                    choice_open_index.append(aux)
                    self.node_classification[place] = (ESTGGraph.CHOICE_CLOSE_OR_HUB, choice_open_index)
                else:
                    self.node_classification[place] = (ESTGGraph.CHOICE_CLOSE_OR_HUB, [aux])

    @staticmethod
    def get_current_signal_values(current_signal_values, order_of_signal_list):
        signal_values = ""
        for signal in order_of_signal_list:
            signal_values += str(current_signal_values[signal])
        return signal_values

    @staticmethod
    def __is_place(node):
        if re.match(r"^transition[0-9]+$", node):
            return False
        return True
