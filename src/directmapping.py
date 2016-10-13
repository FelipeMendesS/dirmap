from estggraph import ESTGGraph
from typing import List, Dict, Set
from graphutil import GraphUtil
from collections import OrderedDict


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

    def __init__(self, graph: ESTGGraph):
        # TODO: Currently not considering initial places when calculating path with only 2 control cells.
        self.graph = graph
        self.set_of_control_cell_places, self.initial_places_not_P1 = self.get_set_of_control_cell_places()  # type: Set[str]
        self.control_cells_graph = {}  # type: Dict[str, Set[str]]
        self.inverse_control_cells_graph = {}  # type: Dict[str, Set[str]]
        self.size_2_cycles = []  # type: List[List[str]]
        self.cycle_0_final_transition = {}  # type: Dict[str, Set[str]]
        self.check_for_size_2_cycles()
        self.get_control_cell_graph()

    def get_set_of_control_cell_places(self):
        set_of_control_cell_places = set(self.graph.initial_places)
        initial_places_not_p1 = set(self.graph.initial_places)
        does_transition_contain_input = {}  # type: Dict[str, bool]
        for transition in self.graph.transitions_identification.keys():
            for signal in self.graph.transitions_identification[transition][0]:
                if self.graph.signal_map[signal] == self.graph.INPUT:
                    does_transition_contain_input[transition] = True
                    break
            if transition in does_transition_contain_input:
                for place in self.graph.extended_graph[transition]:
                    set_of_control_cell_places.add(place)
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
                self.__aux_get_control_cell_graph(control_cell, place, visited_places)
        for place in self.control_cells_graph.keys():
            for connected_place in self.control_cells_graph[place]:
                if connected_place in self.inverse_control_cells_graph:
                    self.inverse_control_cells_graph[connected_place].add(place)
                else:
                    self.inverse_control_cells_graph[connected_place] = set()
                    self.inverse_control_cells_graph[connected_place].add(place)

    def __aux_get_control_cell_graph(self, current_control_cell, current_place, visited_places):
        if current_place not in visited_places:
            if current_place in self.set_of_control_cell_places:
                self.control_cells_graph[current_control_cell].add(current_place)
                visited_places.add(current_place)
                return
            else:
                visited_places.add(current_place)
                for place in self.graph.stg_graph[current_place]:
                    self.__aux_get_control_cell_graph(current_control_cell, place, visited_places)

