from estggraph import ESTGGraph
from typing import List, Dict, Set, Tuple, Union
from graphutil import GraphUtil
from collections import OrderedDict
Transition = List[Tuple[str, int]]


class DirectMapping(object):
    # Class that implements the direct mapping algorithm
    ''' Class that implements the direct mapping algorithm:
        1. Identifies all places that are initial places and places that are only activated by input transitions.
        2. Paths with only two places, not including initial places, are completed with an auxiliary control cell.
        3. Each control cell, not auxiliary, are associated with a logic block with output in Ri
        4. Connect Ro of each control cell to its subsequent logic block
        5. In the opposite direction connect Ao to Ai. When more than one arriving form a joint.
        6. Extract logic blocks Boolean equations
        7. Replace joints with AND gates
        8. Using output signals and the output transitions in the petri-net get the boolean equations of the outputs
    '''

    LOW_LEVEL = 0
    HIGH_LEVEL = 1
    DONT_CARE = 2
    UNDETERMINED = 3

    LEVEL_DICT = {
        0: LOW_LEVEL,
        1: HIGH_LEVEL,
        "*": UNDETERMINED
    }

    def __init__(self, graph: ESTGGraph):
        # TODO: Currently not considering initial places when calculating path with only 2 control cells.
        self.graph = graph
        self.control_cell_input_to_connected_control_cells = {}  # type: Dict[str, Set[str]]
        self.set_of_control_cell_places, self.initial_places_not_P1 = self.get_set_of_control_cell_places()  # type: Set[str]
        self.control_cells_graph = {}  # type: Dict[str, Set[str]]
        self.inverse_control_cells_graph = {}  # type: Dict[str, Set[str]]
        self.size_2_cycles = []  # type: List[List[str]]
        self.cycle_0_final_transition = {}  # type: Dict[str, Set[str]]
        self.output_control_cell_relation = {}  # type: Dict[str, Dict[str, int]]

        

        self.check_for_size_2_cycles()
        self.get_control_cell_graph()
        # self.get_output_control_cell_relation()

    def get_set_of_control_cell_places(self):
        set_of_control_cell_places = set(self.graph.initial_places)
        initial_places_not_p1 = set(self.graph.initial_places)
        does_transition_contain_input = {}  # type: Dict[str, bool]
        for transition in self.graph.transitions_name_to_signal.keys():
            for signal, transition_type in self.graph.transitions_name_to_signal[transition]:
                if self.graph.signal_map[signal] == self.graph.INPUT:
                    does_transition_contain_input[transition] = True
                    break
            if transition in does_transition_contain_input:
                for place in self.graph.extended_graph[transition]:
                    set_of_control_cell_places.add(place)
                    self.control_cell_input_to_connected_control_cells[place + transition] = set()
                    if place in initial_places_not_p1:
                        initial_places_not_p1.remove(place)
        return set_of_control_cell_places, initial_places_not_p1

    def check_for_size_2_cycles(self):
        cycles = []  # type: List[List[str]]
        valid_places_set = self.set_of_control_cell_places - self.initial_places_not_P1
        path_stack = OrderedDict()
        initial_place = self.graph.initial_places[0]
        path_stack[initial_place] = 1
        for place in self.graph.stg_graph[initial_place]:
            self.__aux_check_for_size_2_cycles(OrderedDict(path_stack), cycles, place)
        for cycle in cycles:
            size = 0
            for place in cycle:
                if place in valid_places_set:
                    size += 1
            if size <= 2:
                self.size_2_cycles.append(cycle)
                if size == 0:
                    if cycle[-2] in self.cycle_0_final_transition:
                        self.cycle_0_final_transition[cycle[-2]].add(cycle[-1])
                    else:
                        self.cycle_0_final_transition[cycle[-2]] = set()
                        self.cycle_0_final_transition[cycle[-2]].add(cycle[-1])

    def __aux_check_for_size_2_cycles(self, path_stack, cycles, current_place):
        if current_place in path_stack:
            cycle = []
            place_flag = False
            for key in path_stack.keys():
                if place_flag:
                    cycle.append(key)
                    continue
                if key == current_place:
                    cycle.append(key)
                    place_flag = True
            cycle.append(current_place)
            cycles.append(cycle)
            return
        else:
            path_stack[current_place] = 1
            for place in self.graph.stg_graph[current_place]:
                self.__aux_check_for_size_2_cycles(OrderedDict(path_stack), cycles, place)

    def get_control_cell_graph(self):
        for control_cell in self.set_of_control_cell_places:
            visited_places = set()
            visited_places.add(control_cell)
            self.control_cells_graph[control_cell] = set()
            for place in self.graph.stg_graph[control_cell]:
                transition = self.__get_transition_name(control_cell, place)
                self.__aux_get_control_cell_graph(control_cell, place, visited_places, transition)
        for place in self.control_cells_graph.keys():
            for connected_place in self.control_cells_graph[place]:
                if connected_place in self.inverse_control_cells_graph:
                    self.inverse_control_cells_graph[connected_place].add(place)
                else:
                    self.inverse_control_cells_graph[connected_place] = set()
                    self.inverse_control_cells_graph[connected_place].add(place)

    def __aux_get_control_cell_graph(self, current_control_cell, current_place, visited_places, transition):
        if current_place not in visited_places:
            if current_place in self.set_of_control_cell_places:
                self.control_cells_graph[current_control_cell].add(current_place)
                visited_places.add(current_place)
                if current_place + transition in self.control_cell_input_to_connected_control_cells:
                    self.control_cell_input_to_connected_control_cells[current_place + transition].add(current_control_cell)
                return
            else:
                visited_places.add(current_place)
                for place in self.graph.stg_graph[current_place]:
                    next_transition = self.__get_transition_name(current_place, place)
                    self.__aux_get_control_cell_graph(current_control_cell, place, visited_places, next_transition)

    def __get_transition_name(self, initial_place, destination_place):
        transition_signals = self.graph.stg_graph_transitions[initial_place + destination_place]
        for transition in self.graph.extended_graph[initial_place]:
            if self.graph.transitions_name_to_signal[transition] == transition_signals:
                return transition
        raise Exception("Transition not found!")

    def get_output_control_cell_relation(self):
        # Algorithm working only for the case without concurrency
        # Not working yet for case starting with * don't care
        # Treat case when a loop doesn' add any new information for the don't care. Not sure how to do it yet.
        output_signal_dict = {}
        current_output_signal_dict = {}
        # If for the control cell is 1, this means none of the output signals in undetermined in this one.
        determined_control_cells = {}
        for signal in self.graph.signal_map.keys():
            if self.graph.signal_map[signal] == ESTGGraph.OUTPUT:
                output_signal_dict[signal] = self.UNDETERMINED
                current_output_signal_dict[signal] = self.LEVEL_DICT[self.graph.initial_signal_values[signal]]
        for place in self.set_of_control_cell_places:
            self.output_control_cell_relation[place] = dict(output_signal_dict)
            determined_control_cells[place] = 0
        self.output_control_cell_relation[self.graph.initial_places[0]] = dict(current_output_signal_dict)
        self.__aux_get_output_control_cell_relation(self.graph.initial_places[0], determined_control_cells,
                                          current_output_signal_dict)

    def __aux_get_output_control_cell_relation(self, current_marking, determined_control_cells,
                                               current_output_signal_dict):
        if current_marking in determined_control_cells:
            if determined_control_cells[current_marking] == 1:
                return
            elif self.__is_control_cell_output_signal_determined(current_marking):
                determined_control_cells[current_marking] = 1
        for transition in self.graph.extended_graph[current_marking]:
            output_signals_list = self.__transition_contains_output(self.graph.transitions_name_to_signal[transition])
            next_marking = self.graph.extended_graph[transition][0]
            if len(output_signals_list) == 0:
                if next_marking in self.set_of_control_cell_places:
                    self.output_control_cell_relation[next_marking] = dict(current_output_signal_dict)
                self.__aux_get_output_control_cell_relation(next_marking, determined_control_cells,
                                                            dict(current_output_signal_dict))
            else:
                for signal, transition_type in output_signals_list:
                    if transition_type == ESTGGraph.RISING_EDGE:
                        current_output_signal_dict[signal] = 1
                    else:
                        current_output_signal_dict[signal] = 0
                if next_marking in self.set_of_control_cell_places:
                    self.output_control_cell_relation[next_marking] = dict(current_output_signal_dict)
                self.__aux_get_output_control_cell_relation(next_marking, determined_control_cells,
                                                            dict(current_output_signal_dict))

    def __is_control_cell_output_signal_determined(self, control_cell):
        for signal in self.output_control_cell_relation[control_cell].keys():
            if self.output_control_cell_relation[control_cell][signal] == self.UNDETERMINED:
                return False
        return True

    def __transition_contains_output(self, transition: Transition) -> List[Tuple[str, int]]:
        output_list = []
        for signal, transition_type in transition:
            if self.graph.signal_map[signal] == ESTGGraph.OUTPUT:
                output_list.append((signal, transition_type))
        return output_list
