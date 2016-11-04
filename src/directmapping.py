from estggraph import ESTGGraph
from typing import List, Dict, Set, Tuple, Union
from node import Node
from collections import OrderedDict
from tree import Tree
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
        # TODO: Currently not considering initial places when calculating path with only 2 control cells. FIXIT
        self.graph = graph
        self.set_of_control_cell_places = set()  # type: Set[Node]
        self.initial_places_not_P1 = set()  # type: Set[Node]
        self.set_of_control_cell_places, self.initial_places_not_P1 = self.get_set_of_control_cell_places()
        self.control_cells_graph = {}  # type: Dict[Node, Set[Node]]
        self.inverse_control_cells_graph = {}  # type: Dict[Node, Set[Node]]
        self.size_1_cycles = []  # type: List[List[Node]]
        self.size_2_cycles = []  # type: List[List[Node]]
        self.size_3_cycles = []  # type: List[List[Node]]
        self.cycle_0_final_transition = {}  # type: Dict[Node, Set[str]]
        self.output_control_cell_relation = {}  # type: Dict[str, Dict[str, int]]
        # First direct logic tree and then inverse logic tree.
        self.logic_tree = {}  # type: Dict[Node, Tuple[Tree, Tree]]
        # Starting with variables directly related to circuit implementation
        # Assuming choices can only happen with inputs (Which makes sense) and there are no more than 1 choice close
        # Between two adjacent control cells. (IMPORTANT ASSUMPTION)
        # TODO: Doesn't work for the case when there is concurrency before choice. They are all being anded together.
        self.check_for_size_2_cycles()
        self.get_control_cell_graph()
        # self.get_output_control_cell_relation()

    def get_set_of_control_cell_places(self):
        set_of_control_cell_places = set(self.graph.initial_places)
        initial_places_not_p1 = set(self.graph.initial_places)
        does_transition_contain_input = {}  # type: Dict[str, bool]
        for transition in self.graph.stg_graph_transitions.values():
            for signal, transition_type in transition.transition:
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
        checker_dict = {}
        cycles = []  # type: List[List[Node]]
        valid_places_set = self.set_of_control_cell_places
        path_stack = OrderedDict()
        initial_place = self.graph.initial_places[0]
        path_stack[initial_place] = 1
        for place in self.graph.stg_graph[initial_place]:
            self.__aux_check_for_size_2_cycles(OrderedDict(path_stack), cycles, place, checker_dict)
        for cycle in cycles:
            size = 0
            for place in cycle[:-1]:
                if place in valid_places_set:
                    size += 1
            if size <= 3:
                if size == 3:
                    self.size_3_cycles.append(cycle)
                elif size == 2:
                    self.size_2_cycles.append(cycle)
                elif size == 1:
                    self.size_1_cycles.append(cycle)
                elif size == 0:
                    if cycle[-2] in self.cycle_0_final_transition:
                        self.cycle_0_final_transition[cycle[-2]].add(cycle[-1])
                    else:
                        self.cycle_0_final_transition[cycle[-2]] = set()
                        self.cycle_0_final_transition[cycle[-2]].add(cycle[-1])

    def __aux_check_for_size_2_cycles(self, path_stack, cycles, current_place, checker_dict):
        if current_place in path_stack:
            cycle = []
            place_flag = False
            for key in path_stack.keys():
                if place_flag:
                    cycle.append(key)
                    continue
                if key == current_place:
                    cycle = [key]
                    place_flag = True
            cycle.append(current_place)
            if frozenset(cycle) in checker_dict:
                equal_flag = False
                for check_cycle in checker_dict[frozenset(cycle)]:
                    if DirectMapping.compare_cycles(check_cycle, cycle):
                        equal_flag = True
                        break
                if not equal_flag:
                    cycles.append(cycle)
                    checker_dict[frozenset(cycle)].append(cycle)
            else:
                checker_dict[frozenset(cycle)] = [cycle]
                cycles.append(cycle)
        else:
            path_stack[current_place] = 1
            for place in self.graph.stg_graph[current_place]:
                self.__aux_check_for_size_2_cycles(OrderedDict(path_stack), cycles, place, checker_dict)

    @staticmethod
    def compare_cycles(cycle1: List[Node], cycle2: List[Node]):
        if len(cycle1) != len(cycle2):
            return False
        initial_index = 0
        for index, node in enumerate(cycle1):
            if node == cycle2[0]:
                initial_index = index
                break
        for i in range(len(cycle1)):
            if i + initial_index < len(cycle1) - 1:
                if cycle2[i] != cycle1[i + initial_index]:
                    return False
            else:
                if cycle2[i] != cycle1[i + initial_index - len(cycle1) + 1]:
                    return False
        return True

    def get_control_cell_graph(self):
        # Maybe add a map with already sorted nodes. Gain some time with that. Memory is not a problem.
        a = {}
        for control_cell in self.set_of_control_cell_places:
            visited_places = set()
            visited_places.add(control_cell)
            a[control_cell] = 0
            self.control_cells_graph[control_cell] = set()
            current_tree_node = None  # type: Tree
            inverse_stack = []  # type: List[Tuple[int, int, int]]
            if len(self.graph.extended_graph[control_cell]) > 1:
                self.graph.extended_graph[control_cell].sort()
                current_tree_node = Tree(Tree.AND, size=len(self.graph.extended_graph[control_cell]))
                self.__add_tree_to_place(True, control_cell, current_tree_node)
            inverse_stack_1 = list(inverse_stack)
            for indext, transition in enumerate(self.graph.extended_graph[control_cell]):
                inverse_stack = list(inverse_stack_1)
                if len(self.graph.inverted_extended_graph[transition]) > 1:
                    self.graph.inverted_extended_graph[transition].sort()
                    inverse_stack.append((Tree.OR, self.graph.inverted_extended_graph[transition].index(control_cell),
                                          len(self.graph.inverted_extended_graph[transition])))
                if len(self.graph.extended_graph[transition]) > 1:
                    self.graph.extended_graph[transition].sort()
                    if current_tree_node:
                        current_tree_node.next[indext] = Tree(Tree.OR, size=len(self.graph.extended_graph[transition]))
                    else:
                        current_tree_node = Tree(Tree.OR, size=len(self.graph.extended_graph[transition]))
                        self.__add_tree_to_place(True, control_cell, current_tree_node)
                inverse_stack_2 = list(inverse_stack)
                for indexp, place in enumerate(self.graph.extended_graph[transition]):
                    inverse_stack = list(inverse_stack_2)
                    if len(self.graph.inverted_extended_graph[place]) > 1:
                        self.graph.inverted_extended_graph[place].sort()
                        inverse_stack.append((Tree.AND, self.graph.inverted_extended_graph[place].index(transition),
                                              len(self.graph.inverted_extended_graph[place])))
                    if current_tree_node:
                        if len(self.graph.extended_graph[control_cell]) > 1:
                            if len(self.graph.extended_graph[transition]) > 1:
                                self.__aux_get_control_cell_graph(control_cell, place, visited_places,
                                                                  list(inverse_stack), current_tree_node.next[indext],
                                                                  a, indexp)
                            else:
                                self.__aux_get_control_cell_graph(control_cell, place, visited_places,
                                                                  list(inverse_stack), current_tree_node, a, indext)
                        else:
                            self.__aux_get_control_cell_graph(control_cell, place, visited_places, list(inverse_stack),
                                                              current_tree_node, a, indexp)
                    else:
                        self.__aux_get_control_cell_graph(control_cell, place, visited_places, list(inverse_stack),
                                                          current_tree_node, a)

    def __aux_get_control_cell_graph(self, current_control_cell, current_place: Node, visited_places, inverse_stack,
                                     current_tree_node: Union[Tree, None], a, tree_index=0):
        # Important coefficient that determines if we try for more than one path between the same pair of control cells
        if current_place not in visited_places or a[current_place] < 0:
            if current_place in self.set_of_control_cell_places:
                self.control_cells_graph[current_control_cell].add(current_place)
                if current_place in self.inverse_control_cells_graph:
                    self.inverse_control_cells_graph[current_place].add(current_control_cell)
                else:
                    self.inverse_control_cells_graph[current_place] = set()
                    self.inverse_control_cells_graph[current_place].add(current_control_cell)
                if current_place in visited_places:
                    a[current_place] += 1
                else:
                    visited_places.add(current_place)
                    a[current_place] = 0
                if current_tree_node:
                    current_tree_node.next[tree_index] = Tree(Tree.PLACE, node=current_place)
                else:
                    self.__add_tree_to_place(True, current_control_cell, Tree(Tree.PLACE, node=current_place))
                if len(inverse_stack) > 0:
                    if current_place in self.logic_tree:
                        tree_traverse = self.logic_tree[current_place][1]
                    else:
                        self.logic_tree[current_place] = (None, None)
                        tree_traverse = self.logic_tree[current_place][1]
                    current_index = None
                    if not tree_traverse:
                            aux = inverse_stack.pop()
                            tree_traverse = Tree(aux[0], size=aux[2])
                            current_index = aux[1]
                            self.logic_tree[current_place] = (self.logic_tree[current_place][0], tree_traverse)
                    for index in range(len(inverse_stack)):
                        aux = inverse_stack.pop()
                        if current_index is None:
                            if tree_traverse.classification == aux[0]:
                                current_index = aux[1]
                            else:
                                raise Exception("Incorrect order of logic tree generation")
                        elif tree_traverse.next[current_index] is None:
                            tree_traverse.next[current_index] = Tree(aux[0], size=aux[2])
                            tree_traverse = tree_traverse.next[current_index]
                            current_index = aux[1]
                        else:
                            tree_traverse = tree_traverse.next[current_index]
                            if tree_traverse.classification == aux[0]:
                                current_index = aux[1]
                            else:
                                raise Exception("Incorrect order of logic tree generation")
                    tree_traverse.next[current_index] = Tree(Tree.PLACE, node=current_control_cell)
                else:
                    self.__add_tree_to_place(False, current_place, Tree(Tree.PLACE, node=current_control_cell))
            else:
                if current_place in visited_places:
                    a[current_place] += 1
                else:
                    visited_places.add(current_place)
                    a[current_place] = 0
                if current_tree_node:
                    current_tree_flag = False
                else:
                    current_tree_flag = True
                if len(self.graph.extended_graph[current_place]) > 1:
                    self.graph.extended_graph[current_place].sort()
                    if current_tree_node:
                        current_tree_node.next[tree_index] = Tree(Tree.AND,
                                                                  size=len(self.graph.extended_graph[current_place]))
                    else:
                        current_tree_node = Tree(Tree.AND, size=len(self.graph.extended_graph[current_place]))
                        self.__add_tree_to_place(True, current_control_cell, current_tree_node)
                inverse_stack_1 = list(inverse_stack)
                for indext, transition in enumerate(self.graph.extended_graph[current_place]):
                    inverse_stack = list(inverse_stack_1)
                    if len(self.graph.inverted_extended_graph[transition]) > 1:
                        self.graph.inverted_extended_graph[transition].sort()
                        inverse_stack.append((Tree.OR,
                                              self.graph.inverted_extended_graph[transition].index(current_place),
                                              len(self.graph.inverted_extended_graph[transition])))
                    if len(self.graph.extended_graph[transition]) > 1:
                        self.graph.extended_graph[transition].sort()
                        if current_tree_node:
                            if len(self.graph.extended_graph[current_place]) > 1:
                                if not current_tree_flag:
                                    current_tree_node.next[tree_index].next[indext] = Tree(Tree.OR,
                                                                                           size=len(self.graph.extended_graph[transition]))
                                else:
                                    current_tree_node.next[indext] = Tree(Tree.OR,
                                                                          size=len(self.graph.extended_graph[transition]))
                            else:
                                current_tree_node.next[tree_index] = Tree(Tree.OR,
                                                                          size=len(self.graph.extended_graph[transition]))
                        else:
                            current_tree_node = Tree(Tree.OR, size=len(self.graph.extended_graph[transition]))
                            self.__add_tree_to_place(True, current_control_cell, current_tree_node)
                    inverse_stack_2 = list(inverse_stack)
                    for indexp, place in enumerate(self.graph.extended_graph[transition]):
                        inverse_stack = list(inverse_stack_2)
                        if len(self.graph.inverted_extended_graph[place]) > 1:
                            self.graph.inverted_extended_graph[place].sort()
                            inverse_stack.append((Tree.AND, self.graph.inverted_extended_graph[place].index(transition),
                                                  len(self.graph.inverted_extended_graph[place])))
                        if current_tree_flag:
                            if current_tree_node:
                                if len(self.graph.extended_graph[current_place]) > 1:
                                    if len(self.graph.extended_graph[transition]) > 1:
                                        self.__aux_get_control_cell_graph(current_control_cell, place, visited_places,
                                                                          list(inverse_stack),
                                                                          current_tree_node.next[indext], a, indexp)
                                    else:
                                        self.__aux_get_control_cell_graph(current_control_cell, place, visited_places,
                                                                          list(inverse_stack), current_tree_node,
                                                                          a, indext)
                                elif len(self.graph.extended_graph[transition]) > 1:
                                    self.__aux_get_control_cell_graph(current_control_cell, place, visited_places,
                                                                      list(inverse_stack), current_tree_node, a, indexp)
                                else:
                                    self.__aux_get_control_cell_graph(current_control_cell, place, visited_places,
                                                                      list(inverse_stack), current_tree_node,
                                                                      a, tree_index)
                            else:
                                self.__aux_get_control_cell_graph(current_control_cell, place, visited_places,
                                                                  list(inverse_stack), current_tree_node, a)
                        else:
                            if current_tree_node:
                                if len(self.graph.extended_graph[current_place]) > 1:
                                    if len(self.graph.extended_graph[transition]) > 1:
                                        self.__aux_get_control_cell_graph(current_control_cell, place, visited_places,
                                                                          list(inverse_stack),
                                                                          current_tree_node.next[tree_index].next[indext],
                                                                          a, indexp)
                                    else:
                                        self.__aux_get_control_cell_graph(current_control_cell, place, visited_places,
                                                                          list(inverse_stack),
                                                                          current_tree_node.next[tree_index], a, indext)
                                elif len(self.graph.extended_graph[transition]) > 1:
                                    self.__aux_get_control_cell_graph(current_control_cell, place, visited_places,
                                                                      list(inverse_stack),
                                                                      current_tree_node.next[tree_index], a, indexp)
                                else:
                                    self.__aux_get_control_cell_graph(current_control_cell, place, visited_places,
                                                                      list(inverse_stack), current_tree_node,
                                                                      a, tree_index)
                            else:
                                self.__aux_get_control_cell_graph(current_control_cell, place, visited_places,
                                                                  list(inverse_stack), current_tree_node, a)

    def get_logic_tree(self, current_place: Node, visited_places=set(), current_tree_node: Union[Tree, None]=None, a={},
                       tree_index=0, tree_root_node: Union[Tree, None]=None):
        if not current_place.is_place:
            if len(self.graph.inverted_extended_graph[current_place]) > 1:
                self.graph.inverted_extended_graph[current_place].sort()
                tree_root_node = Tree(Tree.OR, size=len(self.graph.inverted_extended_graph[current_place]))
                current_tree_node = tree_root_node
                for index, place in enumerate(self.graph.inverted_extended_graph[current_place]):
                    self.get_logic_tree(place, current_tree_node=current_tree_node, tree_index=index,
                                        tree_root_node=tree_root_node)
                return tree_root_node
            current_place = self.graph.inverted_extended_graph[current_place][0]
        if current_place not in visited_places or a[current_place] < 0:
            if current_place in self.set_of_control_cell_places:
                if current_place in visited_places:
                    a[current_place] += 1
                else:
                    visited_places.add(current_place)
                    a[current_place] = 0
                if current_tree_node:
                    current_tree_node.next[tree_index] = Tree(Tree.PLACE, node=current_place)
                else:
                    tree_root_node = Tree(Tree.PLACE, node=current_place)
                    current_tree_node = tree_root_node
            else:
                if current_place in visited_places:
                    a[current_place] += 1
                else:
                    visited_places.add(current_place)
                    a[current_place] = 0
                if current_tree_node:
                    current_tree_flag = False
                else:
                    current_tree_flag = True
                if len(self.graph.inverted_extended_graph[current_place]) > 1:
                    self.graph.inverted_extended_graph[current_place].sort()
                    if current_tree_node:
                        current_tree_node.next[tree_index] = Tree(Tree.AND,
                                                                  size=len(self.graph.inverted_extended_graph[current_place]))
                    else:
                        tree_root_node = Tree(Tree.AND, size=len(self.graph.inverted_extended_graph[current_place]))
                        current_tree_node = tree_root_node
                for indext, transition in enumerate(self.graph.inverted_extended_graph[current_place]):
                    if len(self.graph.inverted_extended_graph[transition]) > 1:
                        self.graph.inverted_extended_graph[transition].sort()
                        if current_tree_node:
                            if len(self.graph.inverted_extended_graph[current_place]) > 1:
                                if not current_tree_flag:
                                    current_tree_node.next[tree_index].next[indext] = Tree(Tree.OR,
                                                                                           size=len(self.graph.inverted_extended_graph[transition]))
                                else:
                                    current_tree_node.next[indext] = Tree(Tree.OR,
                                                                          size=len(self.graph.inverted_extended_graph[transition]))
                            else:
                                current_tree_node.next[tree_index] = Tree(Tree.OR,
                                                                          size=len(self.graph.inverted_extended_graph[transition]))
                        else:
                            tree_root_node = Tree(Tree.OR, size=len(self.graph.inverted_extended_graph[transition]))
                            current_tree_node = tree_root_node
                    for indexp, place in enumerate(self.graph.inverted_extended_graph[transition]):
                        if current_tree_flag:
                            if current_tree_node:
                                if len(self.graph.inverted_extended_graph[current_place]) > 1:
                                    if len(self.graph.inverted_extended_graph[transition]) > 1:
                                        self.get_logic_tree(current_place, visited_places,
                                                            current_tree_node.next[indext], a, indexp, tree_root_node)
                                    else:
                                        self.get_logic_tree(current_place, visited_places, current_tree_node, a, indext,
                                                            tree_root_node)
                                elif len(self.graph.inverted_extended_graph[transition]) > 1:
                                    self.get_logic_tree(current_place, visited_places, current_tree_node, a, indexp,
                                                        tree_root_node)
                                else:
                                    self.get_logic_tree(current_place, visited_places, current_tree_node, a, tree_index,
                                                        tree_root_node)
                            else:
                                self.get_logic_tree(current_place, visited_places, current_tree_node, a)
                        else:
                            if current_tree_node:
                                if len(self.graph.inverted_extended_graph[current_place]) > 1:
                                    if len(self.graph.inverted_extended_graph[transition]) > 1:
                                        self.get_logic_tree(current_place, visited_places,
                                                            current_tree_node.next[tree_index].next[indext], a, indexp,
                                                            tree_root_node)
                                    else:
                                        self.get_logic_tree(current_place, visited_places,
                                                            current_tree_node.next[tree_index], a, indext,
                                                            tree_root_node)
                                elif len(self.graph.inverted_extended_graph[transition]) > 1:
                                    self.get_logic_tree(current_place, visited_places,
                                                        current_tree_node.next[tree_index], a, indexp, tree_root_node)
                                else:
                                    self.get_logic_tree(current_place, visited_places, current_tree_node, a, tree_index,
                                                        tree_root_node)
                            else:
                                self.get_logic_tree(current_place, visited_places, current_tree_node, a)
        return tree_root_node

    def __add_tree_to_place(self, is_direct_tree: bool, control_cell: Node, tree: Tree):
        if control_cell in self.logic_tree:
            if is_direct_tree:
                self.logic_tree[control_cell] = (tree, self.logic_tree[control_cell][1])
            else:
                self.logic_tree[control_cell] = (self.logic_tree[control_cell][0], tree)
        else:
            if is_direct_tree:
                self.logic_tree[control_cell] = (tree, None)
            else:
                self.logic_tree[control_cell] = (None, tree)

    def __get_transition_name(self, initial_place, destination_place):
        transition_node = self.graph.stg_graph_transitions[(initial_place, destination_place)]
        for transition in self.graph.extended_graph[initial_place]:
            if transition == transition_node:
                return transition
        raise Exception("Transition not found!")

    def __transition_contains_output(self, transition: Transition) -> List[Tuple[str, int]]:
        output_list = []
        for signal, transition_type in transition:
            if self.graph.signal_map[signal] == ESTGGraph.OUTPUT:
                output_list.append((signal, transition_type))
        return output_list
