from directmapping import DirectMapping
from estggraph import ESTGGraph
from node import Node
from tree import Tree
import os
import datetime
from typing import List, Dict, Tuple


class VHDLGenerator(object):
    '''
    Class that creates the vhdl file from the directmapping algorithm in the DirectMapping class.

    '''

    PATH_TO_VHDL = "../Xilinx/"
    ENTER = "\n"
    COMMENT = "-- "
    SEPARATOR = "-" * 45
    IN = "in  "
    OUT = "out "
    VHDL_EXTENSION = ".vhd"
    INITIAL_NOT_P1 = 0
    INITIAL_P1 = 1
    OTHER_CONTROL_CELLS = 2
    RI = 3
    AI_DIRECT = 4
    AI_INVERSE = 5
    OUTPUT_SET = 6
    OUTPUT_RESET = 7
    AND = " and "
    OR = " or "

    def __init__(self, direct: DirectMapping, file_name: str, use_ai: bool=True):
        self.use_ai = use_ai
        self.direct = direct
        self.file_name = file_name
        self.module_name = file_name.replace("-", "_")
        self.control_cells = []
        self.number_of_aux_cells = 0
        self.last_cycle_2_control_cell = []  # type: List[Node]
        self.outputs = []
        self.output_transitions = {}  # type: Dict[str, Tuple[List[Node], List[Node]]]
        self.output_transitions_logic_tree = {}  # type: Dict[Node, Tree]
        if not os.path.exists(self.PATH_TO_VHDL + file_name):
            os.makedirs(self.PATH_TO_VHDL + file_name)
        directory = self.PATH_TO_VHDL + file_name + "/"
        with open(directory + file_name + self.VHDL_EXTENSION, 'w') as f:
            self.print_initial_comment(f)
            self.print_includes(f)
            self.print_entity(f)
            self.print_architecture(f)
            self.print_signals(f)
            self.print_instantiations(f)
            self.print_ri(f)
            self.print_ai(f)
            self.print_outputs(f)
            f.write("end struct;" + self.ENTER)

    def print_outputs(self, file):
        for node in self.direct.graph.extended_graph.keys():
            if node.is_place:
                continue
            if node.contains_type(self.direct.graph.signal_map, ESTGGraph.OUTPUT):
                for signal, transition_type in node.transition:
                    if transition_type == Node.RISING_EDGE:
                        index = 1
                    else:
                        index = 0
                    if signal not in self.output_transitions:
                        self.output_transitions[signal] = ([], [])
                    self.output_transitions[signal][index].append(node)
                    if node not in self.output_transitions_logic_tree:
                        self.output_transitions_logic_tree[node] = self.direct.get_logic_tree(node, visited_places=set(), a ={})
        for signal in self.outputs:
            if self.direct.graph.initial_signal_values[signal] == "*":
                raise Exception("For now, it's necessary to have initial output values for the algorithm to work!")
            file.write(signal + "_set <= ")
            if self.direct.graph.initial_signal_values[signal] == 1:
                file.write("not reset and (not((")
            else:
                file.write("not((")
            for index, transition in enumerate(self.output_transitions[signal][1]):
                if index > 0:
                    file.write(self.OR + "(")
                self.print_logic_tree(file, self.OUTPUT_SET, self.output_transitions_logic_tree[transition])
            file.write(") or not " + signal + "_reset;" + self.ENTER)
            file.write(signal + "_reset <= ")
            if self.direct.graph.initial_signal_values[signal] == 0:
                file.write("not reset and (not((")
            else:
                file.write("not((")
            for index, transition in enumerate(self.output_transitions[signal][0]):
                if index > 0:
                    file.write(self.OR + "(")
                self.print_logic_tree(file, self.OUTPUT_RESET, self.output_transitions_logic_tree[transition])
            file.write("));" + self.ENTER)
            file.write(self.ENTER)

    def print_ai(self, file):
        initial_places = set(self.direct.graph.initial_places)
        for control_cell in self.control_cells:
            file.write("Ai_" + control_cell.name + " <= ")
            if control_cell in initial_places:
                if self.use_ai:
                    file.write("((")
                else:
                    file.write("(")
            else:
                if self.use_ai:
                    file.write("not reset and ((")
                else:
                    file.write("not reset and (")
            if control_cell in self.last_cycle_2_control_cell:
                index = self.last_cycle_2_control_cell.index(control_cell)
                if self.use_ai:
                    file.write("Ao_Paux" + str(index + 1) + ") or not (")
                else:
                    file.write("Ao_Paux" + str(index + 1) + ")")
            else:
                self.print_logic_tree(file, self.AI_DIRECT, self.direct.logic_tree[control_cell][0])
                if self.use_ai:
                    file.write(" or not (")
            if self.use_ai:
                self.print_logic_tree(file, self.AI_INVERSE, self.direct.logic_tree[control_cell][1])
            file.write(";" + self.ENTER)
        file.write(self.ENTER)
        for index, control_cell in enumerate(self.last_cycle_2_control_cell):
            file.write("Ai_Paux" + str(index + 1) + " <= ")
            if self.use_ai:
                file.write("not reset and ((")
            else:
                file.write("not reset and (")
            self.print_logic_tree(file, self.AI_DIRECT, self.direct.logic_tree[control_cell][0])
            if self.use_ai:
                file.write(" or not Ao_" + control_cell.name + ");" + self.ENTER)
            else:
                file.write(";" + self.ENTER)
        file.write(self.ENTER)

    def print_ri(self, file):
        initial_places_not_p1 = self.direct.initial_places_not_P1
        initial_places_p1 = set(self.direct.graph.initial_places) - initial_places_not_p1
        for control_cell in self.control_cells:
            file.write("Ri_" + control_cell.name + " <= ")
            if control_cell in initial_places_not_p1:
                self.__print_ri(self.INITIAL_NOT_P1, control_cell, file)
                file.write(")")
            elif control_cell in initial_places_p1:
                self.__print_ri(self.INITIAL_P1, control_cell, file)
            else:
                self.__print_ri(self.OTHER_CONTROL_CELLS, control_cell, file)
            file.write(");" + self.ENTER)
        file.write(self.ENTER)
        for i in range(self.number_of_aux_cells):
            file.write("Ri_Paux" + str(i + 1) + " <= not (Ro_" + self.last_cycle_2_control_cell[i].name +
                       " and Ai_Paux" + str(i + 1) + ");")
            file.write(self.ENTER)
        file.write(self.ENTER)
        return

    def __print_ri(self, type_cc: int, control_cell: Node, file):
        if type_cc == self.INITIAL_P1:
            file.write("not (reset or (")
        elif type_cc == self.INITIAL_NOT_P1:
            file.write("not (reset or (Ai_" + control_cell.name + " and (")
        elif type_cc == self.OTHER_CONTROL_CELLS:
            file.write("not (")
        input_flag = True
        multiple_transitions_flag = False
        if type_cc == self.INITIAL_NOT_P1:
            input_flag = False
        if type_cc != self.INITIAL_NOT_P1 and self.number_of_incoming_input_transitions(control_cell) > 1:
            multiple_transitions_flag = True
            self.direct.graph.inverted_extended_graph[control_cell].sort()
        if multiple_transitions_flag:
            if self.direct.logic_tree[control_cell][1].classification != Tree.AND:
                raise Exception("Expected root AND given the multiple incoming input transitions to control cell!")
            for index, transition in enumerate(self.direct.graph.inverted_extended_graph[control_cell]):
                if transition.contains_type(self.direct.graph.signal_map, ESTGGraph.INPUT):
                    file.write("(")
                if self.__print_input_conditions(transition, file):
                    tree_traverse = self.direct.logic_tree[control_cell][1].next[index]
                    self.print_logic_tree(file, self.RI, tree_traverse)
                    file.write(self.OR)
        elif not input_flag:
            self.print_logic_tree(file, self.RI, self.direct.logic_tree[control_cell][1])
        elif type_cc == self.INITIAL_P1:
            for index, transition in enumerate(self.direct.graph.inverted_extended_graph[control_cell]):
                if index > 0:
                    file.write(" or (")
                if self.__print_input_conditions(self.direct.graph.inverted_extended_graph[control_cell][index], file):
                    self.print_logic_tree(file, self.RI, self.direct.logic_tree[control_cell][1].next[index])
                elif type_cc == self.INITIAL_P1:
                    self.print_logic_tree(file, self.RI, self.direct.logic_tree[control_cell][1].next[index])
        else:
            if self.__print_input_conditions(self.direct.graph.inverted_extended_graph[control_cell][0], file):
                    self.print_logic_tree(file, self.RI, self.direct.logic_tree[control_cell][1])

    def number_of_incoming_input_transitions(self, place: Node):
        result = 0
        if not place.is_place:
            raise Exception("Received transition when expected place!")
        else:
            for transition in self.direct.graph.inverted_extended_graph[place]:
                if transition.contains_type(self.direct.graph.signal_map, ESTGGraph.INPUT):
                    result += 1
        return result

    def __print_input_conditions(self, transition, file):
        if transition.is_place:
            raise Exception("Expected transition but received Place!")
        if not transition.contains_type(self.direct.graph.signal_map, ESTGGraph.INPUT):
            return False
        for signal, transition_type in transition.transition:
            if self.direct.graph.signal_map[signal] != ESTGGraph.OUTPUT:
                if transition_type == Node.RISING_EDGE or transition_type == Node.LEVEL_HIGH:
                    file.write(signal + self.AND)
                elif transition_type == Node.FALLING_EDGE or transition_type == Node.LEVEL_LOW:
                    file.write("not " + signal + self.AND)
        file.write("(")
        return True

    def print_logic_tree(self, file, type_cc, tree):
        if tree.classification == Tree.PLACE:
            if type_cc == self.RI or type_cc == self.OUTPUT_SET:
                if tree.node in self.last_cycle_2_control_cell:
                    index = self.last_cycle_2_control_cell.index(tree.node)
                    file.write("Ro_Paux" + str(index + 1) + ')')
                else:
                    file.write("Ro_" + tree.node.name + ')')
            elif type_cc == self.OUTPUT_RESET:
                file.write("Ro_" + tree.node.name + ')')
            elif type_cc == self.AI_INVERSE or type_cc == self.AI_DIRECT:
                file.write("Ao_" + tree.node.name + ")")
        else:
            if type_cc == self.RI or type_cc == self.OUTPUT_SET or type_cc == self.OUTPUT_RESET:
                if tree.classification == Tree.AND:
                    logic = self.OR
                else:
                    logic = self.AND
            elif type_cc == self.AI_DIRECT:
                if tree.classification == Tree.AND:
                    logic = self.AND
                else:
                    logic = self.OR
            else:
                logic = self.AND
            for index, next_tree in enumerate(tree.next):
                if index > 0:
                    file.write(logic)
                if next_tree.classification == Tree.PLACE:
                    if type_cc == self.RI or type_cc == self.OUTPUT_SET:
                        if next_tree.node in self.last_cycle_2_control_cell:
                            index = self.last_cycle_2_control_cell.index(next_tree.node)
                            file.write("Ro_Paux" + str(index + 1))
                        else:
                            file.write("Ro_" + next_tree.node.name)
                    elif type_cc == self.OUTPUT_RESET:
                        file.write("Ro_" + next_tree.node.name)
                    elif type_cc == self.AI_INVERSE or type_cc == self.AI_DIRECT:
                        file.write("Ao_" + next_tree.node.name)
                else:
                    file.write("(")
                    self.print_logic_tree(file, type_cc, next_tree)
            file.write(")")

    def print_entity(self, file):
        file.write("entity " + self.module_name + " is" + self.ENTER)
        input_signals = []
        output_signals = []
        max_len = 0
        for signal in self.direct.graph.signal_map.keys():
            if len(signal) > max_len:
                max_len = len(signal)
            if self.direct.graph.signal_map[signal] == ESTGGraph.OUTPUT:
                output_signals.append(signal)
            else:
                input_signals.append(signal)
        signal = input_signals.pop()
        file.write("port(reset :" + self.IN + "std_logic;" + self.ENTER)
        file.write(" " * 5 + signal + ":" + " " * (max_len - len(signal) + 1) + self.IN + "std_logic;" + self.ENTER)
        for signal in input_signals:
            file.write(" " * 5 + signal + ":" + " " * (max_len - len(signal) + 1) + self.IN + "std_logic;" + self.ENTER)
        for index, signal in enumerate(output_signals):
            if index > 0:
                file.write(";" + self.ENTER)
            file.write(" " * 5 + signal + ":" + " " * (max_len - len(signal) + 1) + self.OUT + "std_logic")
        file.write(");" + self.ENTER)
        file.write("end " + self.module_name + ";" + self.ENTER)
        file.write(self.ENTER)
        file.write(self.SEPARATOR + self.ENTER)
        file.write(self.ENTER)

    def print_signals(self, file):
        for place in self.direct.set_of_control_cell_places:
            self.control_cells.append(place)
            file.write("signal " + "Ri_" + place.name + ": std_logic;" + self.ENTER)
            file.write("signal " + "Ai_" + place.name + ": std_logic;" + self.ENTER)
            file.write("signal " + "Ro_" + place.name + ": std_logic;" + self.ENTER)
            file.write("signal " + "Ao_" + place.name + ": std_logic;" + self.ENTER)
            file.write(self.ENTER)
        if len(self.direct.size_2_cycles) > 0:
            self.number_of_aux_cells = len(self.direct.size_2_cycles)
            for index, cycle in enumerate(self.direct.size_2_cycles):
                higher_node = None
                found_first = False
                for node in cycle:
                    if found_first and node in self.direct.set_of_control_cell_places:
                        if higher_node < node:
                            higher_node = node
                        break
                    if node in self.direct.set_of_control_cell_places:
                        found_first = True
                        higher_node = node
                self.last_cycle_2_control_cell.append(higher_node)
                file.write("signal " + "Ri_Paux" + str(index + 1) + ": std_logic;" + self.ENTER)
                file.write("signal " + "Ai_Paux" + str(index + 1) + ": std_logic;" + self.ENTER)
                file.write("signal " + "Ro_Paux" + str(index + 1) + ": std_logic;" + self.ENTER)
                file.write("signal " + "Ao_Paux" + str(index + 1) + ": std_logic;" + self.ENTER)
                file.write(self.ENTER)
                # file.write("signal " + "Ro_" + higher_node.name + "_buffer" + ": std_logic;" + self.ENTER)
                # file.write(self.ENTER)
        output_signals = self.__get_signals(ESTGGraph.OUTPUT)
        for output in output_signals:
            self.outputs.append(output)
            file.write("signal " + output + "_set:   std_logic;" + self.ENTER)
            file.write("signal " + output + "_reset: std_logic;" + self.ENTER)
            file.write(self.ENTER)

    def print_instantiations(self, file):
        file.write("begin" + self.ENTER)
        file.write(self.ENTER)
        for place in self.control_cells:
            file.write(place.name + ": control_cell port map (Ri_" + place.name + ", Ai_" + place.name + ", Ro_" +
                       place.name + ", Ao_" + place.name + ");" + self.ENTER)
        file.write(self.ENTER)
        for i in range(self.number_of_aux_cells):
            # control_cell_name = self.last_cycle_2_control_cell[i].name
            file.write("Paux" + str(i + 1) + ": control_cell port map (Ri_Paux" + str(i + 1) + ", Ai_Paux" +
                       str(i + 1) + ", Ro_Paux" + str(i + 1) + ", Ao_Paux" + str(i + 1) + ");" + self.ENTER)
            # file.write("buffer_" + str(i + 1) + ": buffer_n generic map(N => 8) port map (Ro_" + control_cell_name +
            #            ", Ro_" + control_cell_name + "_buffer);" + self.ENTER)
            file.write(self.ENTER)
        for output in self.outputs:
            file.write(output + "_cell: output_cell port map (" + output + "_set, " + output + "_reset, " + output +
                       ");" + self.ENTER)
        file.write(self.ENTER)

    def print_architecture(self, file):
        file.write("architecture struct of " + self.module_name + " is" + self.ENTER)
        file.write(self.ENTER)
        file.write("component control_cell is" + self.ENTER)
        file.write("port(Ri: in    std_logic;" + self.ENTER)
        file.write("     Ai: in    std_logic;" + self.ENTER)
        file.write("     Ro: inout std_logic;" + self.ENTER)
        file.write("     Ao: out   std_logic" + self.ENTER)
        file.write(");" + self.ENTER)
        file.write("end component;" + self.ENTER)
        file.write(self.ENTER)
        # file.write("component buffer_n is" + self.ENTER)
        # file.write("generic(N: integer);" + self.ENTER)
        # file.write("port(a: in  std_logic;" + self.ENTER)
        # file.write("     b: out std_logic" + self.ENTER)
        # file.write(");" + self.ENTER)
        # file.write("end component;" + self.ENTER)
        # file.write(self.ENTER)
        file.write("component output_cell is" + self.ENTER)
        file.write("port(set:    in  std_logic;" + self.ENTER)
        file.write("     reset:  in  std_logic;" + self.ENTER)
        file.write("     output: out std_logic" + self.ENTER)
        file.write(");" + self.ENTER)
        file.write("end component;" + self.ENTER)
        file.write(self.ENTER)

    def __get_signals(self, type_cc: int):
        output_signals = []
        input_signals = []
        max_len = 0
        for signal in self.direct.graph.signal_map.keys():
            if len(signal) > max_len:
                max_len = len(signal)
            if self.direct.graph.signal_map[signal] == ESTGGraph.OUTPUT:
                output_signals.append(signal)
            else:
                input_signals.append(signal)
        if type_cc == ESTGGraph.OUTPUT:
            return output_signals
        else:
            return input_signals

    def print_initial_comment(self, file):
        file.write(self.SEPARATOR + self.ENTER)
        file.write(self.COMMENT + self.file_name + self.ENTER)
        file.write(self.COMMENT + "by Felipe Mendes dos Santos, " + str(datetime.date.today().strftime('%d/%m/%Y')))
        file.write(self.ENTER + self.SEPARATOR + self.ENTER)
        file.write(self.ENTER)

    def print_includes(self, file):
        file.write("library ieee;" + self.ENTER)
        file.write("use ieee.std_logic_1164.all;" + self.ENTER)
        file.write("use work.all;" + self.ENTER)
        file.write(self.ENTER)
        file.write(self.SEPARATOR + self.ENTER)
        file.write(self.ENTER)
