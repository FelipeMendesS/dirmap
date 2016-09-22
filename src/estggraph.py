import re
from typing import List, Dict, Tuple, Union, Set
Transition = Tuple[List[str], List[int]]


class ESTGGraph (object):

    # Data that we need to use
    # Check if we can have a choice to different concurrency, at first won't be implemented. Can change data structures
    # if needed.

    # Signals classifications
    INPUT = 0
    OUTPUT = 1
    CONDITIONAL_SIGNAL = 2
    #Transitions classifications
    RISING_EDGE = 3
    FALLING_EDGE = 4
    DONT_CARE = 5
    LEVEL_HIGH = 6
    LEVEL_LOW = 7
    # Node classifications
    CONCURRENCY_OPEN = 8
    CHOICE_OPEN = 9
    CONCURRENCY_CLOSE = 10

    SYMBOL_DICT = {
        3: ["", "+"],
        4: ["", "-"],
        5: ["", "*"],
        6: ["[", "+]"],
        7: ["[", "-]"]
    }

    def __init__(self, regular_inputs, outputs, choice_inputs, transitions, initial_places, initial_signal_values):
        # Map to relate all variables to type (Input, output, conditional signal)
        self.signal_map = {}  # type: Dict[str, int]
        # Map that shows graph and each node has its type in a tuple associated with the value
        self.stg_graph = {}  # type: Dict[str, List[str]]
        # Map that shows the variables involved in each and every transition in the graph. The keys are made by the
        # concatenation of the nodes names
        self.transition_variables = {}  # type: Dict[str, Transition]
        # Map that holds the identification of all transitions
        self.transitions_identification = {}  # type: Dict[str, Transition]
        # Map that stores the real complete graph, considering also the transitions as nodes.
        self.extended_graph = {}  # type: Dict[str, List[str]]
        # List of places starting with tokens
        self.initial_places = initial_places  # type: List[str]
        # Map of signals and their initial values
        self.initial_signal_values = initial_signal_values  # type: Dict[str, Union[int,str]]
        # Node classification to check concurrency and decisions
        self.node_classification = {}  # type: Dict[str,Tuple[int, int]]
        transition_count = 0
        for regular_input in regular_inputs:
            self.signal_map[regular_input] = self.INPUT
        for output in outputs:
            self.signal_map[output] = self.OUTPUT
        for choice in choice_inputs:
            self.signal_map[choice] = self.CONDITIONAL_SIGNAL
        for line in transitions:
            [vertices, variables] = map(str.strip, line[0].split('|'))
            transition_type = line[1]
            v = []
            t = []
            for variable in map(str.strip, variables.split(',')):
                if re.match(r"#\w+[+\-*]", variable):
                    if variable[-1] == "+":
                        t.append(self.LEVEL_HIGH)
                    elif variable[-1] == "-":
                        t.append(self.LEVEL_LOW)
                    else:
                        t.append(self.DONT_CARE)
                else:
                    if variable[-1] == "+":
                        t.append(self.RISING_EDGE)
                    elif variable[-1] == "-":
                        t.append(self.FALLING_EDGE)
                    else:
                        t.append(self.DONT_CARE)
                v.append(variable.strip('#+-*'))
            transition_conditions = (v, t)
            transition_count += 1
            transition_name = "transition" + str(transition_count)
            if transition_type == 1:
                count_aux = len(vertices.split('/')[1].strip().split(','))
                self.node_classification[transition_name] = (self.CONCURRENCY_OPEN, count_aux)
            elif transition_type == 3:
                count_aux = len(vertices.split('/')[0].strip().split(','))
                self.node_classification[transition_name] = (self.CONCURRENCY_CLOSE, count_aux)
            self.transitions_identification[transition_name] = transition_conditions
            [origin_vertex, destination_vertex] = map(str.strip, vertices.split('/'))
            for origin in map(str.strip, origin_vertex.split(',')):
                if origin not in self.stg_graph:
                    self.stg_graph[origin] = []
                if origin not in self.extended_graph:
                    self.extended_graph[origin] = [transition_name]
                else:
                    self.extended_graph[origin].append(transition_name)
                self.extended_graph[transition_name] = []
                for destination in destination_vertex.split(','):
                    self.stg_graph[origin].append(destination)
                    self.transition_variables[origin + destination] = transition_conditions
                    self.extended_graph[transition_name].append(destination)
        self.label_decisions()

    # Check if the graph is strongly connected
    def check_liveness(self):
        return

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
            signal_values = dict(current_signal_values)
            (signals, transitions) = self.transition_variables[current_place + destination]
            for index, signal in enumerate(signals):
                if transitions[index] == self.RISING_EDGE:
                    if signal_values[signal] == 0 or signal_values[signal] == "*":
                        signal_values[signal] = 1
                    else:
                        raise Exception("Inconsistent transition between place " + current_place + " and place " +
                                        destination + ". " + signal +
                                        " was 1 and is expected to rise in this transition")
                elif transitions[index] == self.FALLING_EDGE:
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

    @staticmethod
    def get_current_signal_values(current_signal_values, order_of_signal_list):
        signal_values = ""
        for signal in order_of_signal_list:
            signal_values += str(current_signal_values[signal])
        return signal_values

    def check_output_persistency(self):
        for node in self.node_classification.keys():
            if node in self.stg_graph:
                for transition in self.extended_graph[node]:
                    for signal in self.transitions_identification[transition][0]:
                        if self.signal_map[signal] == self.OUTPUT:
                            raise Exception("In the decision coming from place " + node +
                                            ", one of the transitions contain the output signal " + signal +
                                            ". Thus this ESTG is not output persistent.")
        print("ESTG is output-persistent!")
        return

    def label_decisions(self):
        for place in self.stg_graph.keys():
            if len(self.extended_graph[place]) > 1:
                self.node_classification[place] = (self.CONDITIONAL_SIGNAL, len(self.extended_graph[place]))
        return