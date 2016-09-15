import re


class STGGraph (object):

    # Data that we need to use
    # Check if we can ave a choice to different concurrencies, at first won't be implemented. Can change data structures
    # if needed.

    INPUT = 0
    OUTPUT = 1
    CONDITIONAL_SIGNAL = 2
    RISING_EDGE = 3
    FALLING_EDGE = 4
    DONT_CARE = 5
    LEVEL_HIGH = 6
    LEVEL_LOW = 7

    def __init__(self, regular_inputs, outputs, choice_inputs, transitions, initial_places, initial_signal_values):
        # Map to relate all variables to type (Input, output, choice)
        self.signal_map = {}  # type: dict
        # Map that shows graph and each node has its type in a tuple associated with the value
        self.stg_graph = {}  # type: dict
        # Map that shows the variables involved in each and every transition in the graph. The keys are made by the
        # concatenation of the nodes names
        self.transition_variables = {}  # type: dict
        # Map that holds the identification of all transitions
        self.transitions_identification = {}  # type: dict
        # Map that stores the real complete graph, considering also the transitions as nodes.
        self.extended_graph = {}  # type: dict
        self.initial_places = initial_places  # type: list
        self.initial_signal_values = initial_signal_values  # type: dict
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
            self.transitions_identification[transition_name] = transition_conditions
            [origin_vertex, destination_vertex] = map(str.strip, vertices.split('/'))
            for origin in map(str.strip, origin_vertex.split(',')):
                if origin not in self.stg_graph:
                    self.stg_graph[origin] = ([], 0)
                if origin not in self.extended_graph:
                    self.extended_graph[origin] = [transition_name]
                else:
                    self.extended_graph[origin].append(transition_name)
                self.extended_graph[transition_name] = []
                for destination in destination_vertex.split(','):
                    self.stg_graph[origin][0].append(destination)
                    self.stg_graph[origin] = (self.stg_graph[origin][0], transition_type)
                    self.transition_variables[origin + destination] = transition_conditions
                    self.extended_graph[transition_name].append(destination)

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
        for destination in self.stg_graph[current_place][0]:
            signal_values = dict(current_signal_values)
            (signals, transitions) = self.transition_variables[current_place + destination]
            for index, signal in enumerate(signals):
                if transitions[index] == self.RISING_EDGE:
                    if signal_values[signal] == 0:
                        signal_values[signal] = 1
                    else:
                        raise Exception("Inconsistent transition between place " + current_place + " and place " +
                                        destination + ". " + signal +
                                        " was 1 and is expected to rise in this transition")
                elif transitions[index] == self.FALLING_EDGE:
                    if signal_values[signal] == 1:
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

    @staticmethod
    def get_current_signal_values(current_signal_values, order_of_signal_list):
        signal_values = ""
        for signal in order_of_signal_list:
            signal_values += str(current_signal_values[signal])
        return signal_values

    def check_output_persistency(self):
        return