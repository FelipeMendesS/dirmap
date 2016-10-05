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
        self.graph = graph
        self.set_of_control_cell_places, self.initial_places_not_P1 = self.get_set_of_control_cell_places()  # type: Set[str]
        self.control_cells_graph = {}  # type: Dict[str, Set[str]]
        self.size_2_cycles = []  # type: List[List[str]]
        self.cycle_0_final_transition = {}  # type: Dict[str, Set[str]]
        self.check_for_size_2_cycles()
        # self.get_control_cell_graph()


    def get_set_of_control_cell_places(self):
        set_of_control_cell_places = set(self.graph.initial_places)
        initial_places_not_P1 = set(self.graph.initial_places)
        does_transition_contain_input = {}  # type: Dict[str, bool]
        for transition in self.graph.transitions_identification.keys():
            for signal in self.graph.transitions_identification[transition][0]:
                if self.graph.signal_map[signal] == self.graph.INPUT:
                    does_transition_contain_input[transition] = True
                    break
            if transition in does_transition_contain_input:
                for place in self.graph.extended_graph[transition]:
                    set_of_control_cell_places.add(place)
                    if place in initial_places_not_P1:
                        initial_places_not_P1.remove(place)
        return set_of_control_cell_places, initial_places_not_P1

    def check_for_size_2_cycles(self):
        cycles = []  # type: List[List[str]]
        valid_places_set = self.set_of_control_cell_places - self.initial_places_not_P1
        path_stack = OrderedDict()
        initial_place = self.graph.initial_places[0]
        path_stack[initial_place] = 1
        for place in self.graph.stg_graph[initial_place]:
            self.__aux_check_for_size_2_cycles(OrderedDict(path_stack), cycles, place)
        for cycle in cycles:
            initial_control_cell = ""
            current_control_cell = ""
            size = 0
            for place in cycle:
                if place in valid_places_set:
                    size += 1
            #         if initial_control_cell == "":
            #             initial_control_cell = place
            #             current_control_cell = initial_control_cell
            #         else:
            #             if current_control_cell in self.control_cells_graph:
            #                 self.control_cells_graph[current_control_cell].add(place)
            #             else:
            #                 self.control_cells_graph[current_control_cell] = set()
            #                 self.control_cells_graph[current_control_cell].add(place)
            #             current_control_cell = place
            # if initial_control_cell != "":
            #     if current_control_cell in self.control_cells_graph:
            #         self.control_cells_graph[current_control_cell].add(initial_control_cell)
            #     else:
            #         self.control_cells_graph[current_control_cell] = set()
            #         self.control_cells_graph[current_control_cell].add(initial_control_cell)
            # Potentially a problem
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
        visited_places = set()
        for place in self.graph.initial_places:
            if place in self.control_cells_graph:
                continue
            else:
                self.__aux_get_control_cell_graph(place, place, visited_places)

    def __aux_get_control_cell_graph(self, current_control_cell, current_place, visited_places, aux_cycle_0=set()):
        for place in self.graph.stg_graph[current_place]:
            if place in self.set_of_control_cell_places:
                if current_control_cell in self.control_cells_graph:
                    self.control_cells_graph[current_control_cell].add(place)
                else:
                    self.control_cells_graph[current_control_cell] = set()
                    self.control_cells_graph[current_control_cell].add(place)
                if place in self.control_cells_graph:
                    continue
                else:
                    self.__aux_get_control_cell_graph(place, place, visited_places)
            else:
                if current_place in self.cycle_0_final_transition and place in \
                        self.cycle_0_final_transition[current_place]:
                    if current_place + place in aux_cycle_0:
                        continue
                    else:
                        aux_cycle_0.add(current_place + place)
                        self.__aux_get_control_cell_graph(current_control_cell, place, visited_places, aux_cycle_0)
                if len(aux_cycle_0) > 0:
                    self.__aux_get_control_cell_graph(current_control_cell, place, visited_places, aux_cycle_0)
                else:
                    self.__aux_get_control_cell_graph(current_control_cell, place, visited_places)
