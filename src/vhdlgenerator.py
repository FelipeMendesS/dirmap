from directmapping import DirectMapping
from estggraph import ESTGGraph
from node import Node
from tree import Tree
import os
import datetime


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
    AI = 4
    OUTPUT = 5
    AND = " and "
    OR = " or "

    def __init__(self, direct: DirectMapping, file_name: str):
        self.direct = direct
        self.file_name = file_name
        self.control_cells = []
        self.number_of_aux_cells = 0
        self.last_cycle_2_control_cell = []  # type: List[Node]
        self.outputs = []
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
            # self.print_ai(f)
            # self.print_outputs(f)

    def print_ri(self, file):
        initial_places_not_p1 = self.direct.initial_places_not_P1
        initial_places_p1 = set(self.direct.graph.initial_places) - initial_places_not_p1
        for control_cell in self.control_cells:
            file.write("Ri_" + control_cell.name + " <= ")
            if control_cell in initial_places_not_p1:
                self.__print_ri(self.INITIAL_NOT_P1, control_cell, file)
            elif control_cell in initial_places_p1:
                self.__print_ri(self.INITIAL_P1, control_cell, file)
            else:
                self.__print_ri(self.OTHER_CONTROL_CELLS, control_cell, file)
            file.write(")" + self.ENTER)
        file.write(self.ENTER)
        for i in range(self.number_of_aux_cells):
            file.write("Ri_Paux" + str(i + 1) + " <= not Ro_" + self.last_cycle_2_control_cell[i].name + "_buffer;")
            file.write(self.ENTER)
        file.write(self.ENTER)
        return

    def __print_ri(self, type_cc: int, control_cell: Node, file):
        if type_cc == self.INITIAL_NOT_P1 or type_cc == self.INITIAL_P1:
            file.write("not (reset or (")
        if type_cc == self.OTHER_CONTROL_CELLS:
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
            file.write("Ro_" + tree.node.name + ")")
        else:
            if tree.classification == Tree.AND:
                logic = self.OR
            else:
                logic = self.AND
            for index, next_tree in enumerate(tree.next):
                if index > 0:
                    file.write(logic)
                if next_tree.classification == Tree.PLACE:
                    file.write("Ro_" + next_tree.node.name)
                else:
                    file.write("(")
                    self.print_logic_tree(file, type_cc, next_tree)
            file.write(")")

    def print_entity(self, file):
        file.write("entity " + self.file_name + " is" + self.ENTER)
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
        file.write("port(" + signal + ":" + " " * (max_len - len(signal) + 1) + self.IN + "std_logic;" + self.ENTER)
        for signal in input_signals:
            file.write(" " * 5 + signal + ":" + " " * (max_len - len(signal) + 1) + self.IN + "std_logic;" + self.ENTER)
        for signal in output_signals:
            file.write(" " * 5 + signal + ":" + " " * (max_len - len(signal) + 1) + self.OUT + "std_logic;" + self.ENTER)
        file.write(");" + self.ENTER)
        file.write("end " + self.file_name + ";" + self.ENTER)
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
                last_node = None
                found_first = False
                for node in cycle:
                    if found_first and node in self.direct.set_of_control_cell_places:
                        last_node = node
                        break
                    if node in self.direct.set_of_control_cell_places:
                        found_first = True
                if not last_node:
                    raise Exception("Size 2 cycle has only one control cell!")
                self.last_cycle_2_control_cell.append(last_node)
                file.write("signal " + "Ri_Paux" + str(index) + ": std_logic;" + self.ENTER)
                file.write("signal " + "Ai_Paux" + str(index) + ": std_logic;" + self.ENTER)
                file.write("signal " + "Ro_Paux" + str(index) + ": std_logic;" + self.ENTER)
                file.write("signal " + "Ao_Paux" + str(index) + ": std_logic;" + self.ENTER)
                file.write(self.ENTER)
                file.write("signal " + "Ro_" + last_node.name + "_buffer" + ": std_logic;" + self.ENTER)
                file.write(self.ENTER)
        output_signals = self.__get_signals(ESTGGraph.OUTPUT)
        for output in output_signals:
            self.outputs.append(output)
            file.write("signal " + output + "_set:   std_logic" + self.ENTER)
            file.write("signal " + output + "_reset: std_logic" + self.ENTER)
            file.write(self.ENTER)

    def print_instantiations(self, file):
        file.write("begin" + self.ENTER)
        file.write(self.ENTER)
        for place in self.control_cells:
            file.write(place.name + ": control_cell port map (Ri_" + place.name + ", Ai_" + place.name + ", Ro_" +
                       place.name + ", Ao_" + place.name + ");" + self.ENTER)
        file.write(self.ENTER)
        for i in range(self.number_of_aux_cells):
            control_cell_name = self.last_cycle_2_control_cell[i].name
            file.write("Paux" + str(i + 1) + ": control_cell port map (Ri_Paux" + str(i + 1) + ", Ai_Paux" +
                       str(i + 1) + ", Ro_Paux" + str(i + 1) + ", Ao_Paux" + str(i + 1) + ");" + self.ENTER)
            file.write("buffer_" + str(i + 1) + ": buffer_n generic map(N => 8) port map (Ro_" + control_cell_name +
                       ", Ro_" + control_cell_name + "_buffer);" + self.ENTER)
            file.write(self.ENTER)
        for output in self.outputs:
            file.write(output + "_cell: output_cell port map (" + output + "_set, " + output + "_reset, " + output +
                       ");" + self.ENTER)
        file.write(self.ENTER)

    def print_architecture(self, file):
        file.write("architecture struct of " + self.file_name + " is" + self.ENTER)
        file.write(self.ENTER)
        file.write("component control_cell is" + self.ENTER)
        file.write("port(Ri: in    std_logic;" + self.ENTER)
        file.write("     Ai: in    std_logic;" + self.ENTER)
        file.write("     Ro: inout std_logic;" + self.ENTER)
        file.write("     Ao: out   std_logic" + self.ENTER)
        file.write(");" + self.ENTER)
        file.write("end component;" + self.ENTER)
        file.write(self.ENTER)
        file.write("component buffer_n is" + self.ENTER)
        file.write("generic(N: integer);" + self.ENTER)
        file.write("port(a: in  std_logic;" + self.ENTER)
        file.write("     b: out std_logic" + self.ENTER)
        file.write(");" + self.ENTER)
        file.write("end component;" + self.ENTER)
        file.write(self.ENTER)
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
