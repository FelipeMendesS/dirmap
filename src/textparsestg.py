import re
import os
import pickle
import hashlib
from typing import List, Tuple, Dict
from estggraph import ESTGGraph
from textparseestg import TextParseESTG
Transition = Tuple[str, str]


class TextParseSTG(object):

    def __init__(self, file_to_convert, converted_file_name="", overwrite_file_flag=False):
        self.inputs = []  # type: List[str]
        self.outputs = []  # type: List[str]
        self.graph = {}  # type: Dict[str, List[str]]
        self.name = ""  # type: str
        # If not declared starts from the first transition.
        self.initial_markings = []  # type: List[Transition]
        self.node_classification = {}  # type: Dict[str, Tuple[int, int]]
        self.extended_graph = {}  # type: Dict[str, List[str]]
        self.file_to_convert = file_to_convert  # type: str
        self.converted_file_name = converted_file_name  # type: str
        self.initial_places_list = []  # type: List[str]
        if self.converted_file_name == "":
            if re.match(r"^.+\.g$", file_to_convert):
                self.converted_file_name = self.file_to_convert[:-2]
            else:
                raise Exception("Give a file name for the output or choose a file with compatible extension!")
        if os.path.isfile(TextParseESTG.PATH_TO_DESCRIPTIONS + self.converted_file_name)\
                and not self.__was_file_changed() and not overwrite_file_flag:
            print("File already exists and it's not asked to be overwritten.")
            return
        with open(file_to_convert, 'r') as f:
            file_lines = f.read().splitlines()
        is_marking_present = False
        for line in file_lines:
            if re.match(r"^#.*", line):
                continue
            elif re.match(r"^\s*\.name\s+\w+", line):
                self.name += line.strip()[5:].strip()
            elif re.match(r"^\s*\.inputs(\s+\w+)+", line):
                self.inputs.extend(line.strip()[7:].split())
            elif re.match(r"^\s*\.outputs(\s+\w+)+", line):
                self.outputs.extend(line.strip()[8:].split())
            elif re.match(r"^\s*\.internal(\s+\w+)+", line):
                self.outputs.extend(line.strip()[9:].split())
            elif re.match(r"^\s*\.dummy(\s+\w+)+", line):
                self.outputs.extend(line.strip()[6:].split())
            elif re.match(r"\s*\w+[+-]?(/[0-9]+)?(\s+\w+[+-]?(/[0-9]+)?)+", line):
                aux = line.strip().split()
                source_transition = aux[0]
                initial_markings_flag = False
                if len(self.initial_markings) == 0:
                    initial_markings_flag = True
                aux = aux[1:]
                if source_transition not in self.graph:
                    self.graph[source_transition] = []
                for variable in aux:
                    self.graph[source_transition].append(variable)
                    if initial_markings_flag:
                        self.initial_markings.append((source_transition, variable))
            elif re.match(r"\s*\.marking\s+", line):
                is_marking_present = True
                aux = line.strip(".marking {}")
                self.initial_markings = []
                self.__get_initial_markings(aux)
        if not is_marking_present:
            print("Warning! This STG especification doesn't have a initial marking defined. It's necessary to fix this"
                  "before synthesis")
        self.__get_extended_graph()
        self.__classify_nodes()
        self.__write_file()

    def __was_file_changed(self):
        # Used as reference in
        # http://stackoverflow.com/questions/1912567/python-library-to-detect-if-a-file-has-changed-between-different-runs
        try:
            data = pickle.load(open("fileState", 'rb'))
        except (EOFError, FileNotFoundError, IOError):
            data = []
        last_state = dict(data)
        checksum = hashlib.md5(open(TextParseESTG.PATH_TO_DESCRIPTIONS +
                                    self.converted_file_name).read().encode('utf-8')).hexdigest()
        if self.converted_file_name not in last_state or last_state[self.converted_file_name] != checksum:
            last_state[self.converted_file_name] = checksum
            pickle.dump(list(last_state.items()), open("fileState", "wb"))
            return True
        return False

    def __get_initial_markings(self, marking_line: str) -> List[Transition]:
        # TODO: Known Issue! If we have any space inside the initial marking definition we get errors.
        # Return a list of transitions that are considered the initial markings of this specification. If a place is
        # one of the initial markings it's going to be represented as the place two times in  the tuple
        markings = marking_line.split()
        for marking in markings:
            if TextParseSTG.__is_place(marking):
                self.initial_markings.append((marking, marking))
            elif re.match(r"^<\s*\w+[+-](/[0-9]+)?\s*,\s*\w+[+-](/[0-9]+)?\s*>$", marking):
                aux = marking.strip("<>").split(",")
                self.initial_markings.append((aux[0].strip(), aux[1].strip()))
            else:
                raise Exception("Markings with wrong syntax " + marking_line)

    def __get_extended_graph(self):
        place_relation = {}
        initial_transitions = set()
        place_count = [1]
        for node in self.initial_markings:
            if TextParseSTG.__is_place(node[0]):
                place_relation[node[0]] = TextParseSTG.__get_place_name(place_count)
                initial_transitions.update(set(self.graph[node[0]]))
                self.extended_graph[TextParseSTG.__get_place_name(place_count)] = self.graph[node[0]]
                self.initial_places_list.append(TextParseSTG.__get_place_name(place_count))
                place_count[0] += 1
            else:
                initial_transitions.add(node[1])
                initial_transitions.add(node[0])
                if node[0] not in self.extended_graph:
                    self.extended_graph[node[0]] = [TextParseSTG.__get_place_name(place_count)]
                else:
                    self.extended_graph[node[0]].append(TextParseSTG.__get_place_name(place_count))
                self.extended_graph[TextParseSTG.__get_place_name(place_count)] = [node[1]]
                self.initial_places_list.append(TextParseSTG.__get_place_name(place_count))
                place_count[0] += 1
        for transition in initial_transitions:
            for following_node in self.graph[transition]:
                if TextParseSTG.__is_place(following_node):
                    if following_node in place_relation:
                        self.__add_connection(transition, place_relation[following_node])
                        continue
                    place_relation[following_node] = TextParseSTG.__get_place_name(place_count)
                    self.__add_connection(transition, TextParseSTG.__get_place_name(place_count))
                    place_count[0] += 1
                    self.__aux_get_extended_graph(following_node, place_count, place_relation)
                else:
                    if following_node in initial_transitions and (transition, following_node) in self.initial_markings:
                        continue
                    duplicate_flag = False
                    if following_node in self.extended_graph and transition in self.extended_graph:
                        for place in self.extended_graph[transition]:
                            if following_node in set(self.extended_graph[place]):
                                duplicate_flag = True
                    if duplicate_flag:
                        continue
                    self.__add_connection(transition, TextParseSTG.__get_place_name(place_count))
                    self.__add_connection(following_node, TextParseSTG.__get_place_name(place_count), False)
                    place_count[0] += 1
                    if following_node in self.extended_graph:
                        continue
                    self.__aux_get_extended_graph(following_node, place_count, place_relation)

    def __aux_get_extended_graph(self, current_node, place_count, place_relation):
        if TextParseSTG.__is_place(current_node):
            for transition in self.graph[current_node]:
                self.__add_connection(transition, place_relation[current_node], False)
                if transition in self.extended_graph:
                    continue
                else:
                    self.__aux_get_extended_graph(transition, place_count, place_relation)
        else:
            for node in self.graph[current_node]:
                if TextParseSTG.__is_place(node):
                    if node in place_relation:
                        self.__add_connection(current_node, place_relation[node])
                        continue
                    else:
                        place_relation[node] = TextParseSTG.__get_place_name(place_count)
                        self.__add_connection(current_node, TextParseSTG.__get_place_name(place_count))
                        place_count[0] += 1
                        self.__aux_get_extended_graph(node, place_count, place_relation)
                else:
                    self.__add_connection(current_node, TextParseSTG.__get_place_name(place_count))
                    self.__add_connection(node, TextParseSTG.__get_place_name(place_count), False)
                    place_count[0] += 1
                    if node in self.extended_graph:
                        continue
                    else:
                        self.__aux_get_extended_graph(node, place_count, place_relation)

    def __classify_nodes(self):
        # TODO Luckily working but this is actually inaccurate. We have to consider the case when the transition is
        # closing and opening concurrency simultaneously
        transition_fanin_count = {}
        for node in self.extended_graph.keys():
            if TextParseSTG.__is_place(node):
                if len(self.extended_graph[node]) > 1:
                    self.node_classification[node] = (ESTGGraph.CHOICE_OPEN, len(self.extended_graph[node]))
                for transition in self.extended_graph[node]:
                    if transition not in transition_fanin_count:
                        transition_fanin_count[transition] = 1
                    else:
                        transition_fanin_count[transition] += 1
            else:
                if len(self.extended_graph[node]) > 1:
                    self.node_classification[node] = (ESTGGraph.CONCURRENCY_OPEN, len(self.extended_graph[node]))
        for transition in transition_fanin_count:
            if transition_fanin_count[transition] > 1:
                self.node_classification[transition] = (ESTGGraph.CONCURRENCY_CLOSE_OR_HUB,
                                                        transition_fanin_count[transition])

    def __add_connection(self, transition, place, is_transition_parent=True):
        if is_transition_parent:
            if transition not in self.extended_graph:
                self.extended_graph[transition] = [place]
            else:
                self.extended_graph[transition].append(place)
        else:
            if place not in self.extended_graph:
                self.extended_graph[place] = [transition]
            else:
                self.extended_graph[place].append(transition)

    @staticmethod
    def __get_place_name(place_count):
        return "PL" + str(place_count[0])

    @staticmethod
    def __is_place(node):
        if re.match(r"\w+$", node):
            return True
        return False

    def __write_file(self):
        traversed_places = {}
        concurrency_close_map = {}
        with open(TextParseESTG.PATH_TO_DESCRIPTIONS + self.converted_file_name, 'w') as f:
            if self.name != "":
                f.write(".name " + self.name + TextParseESTG.ENTER)
            else:
                f.write(".name " + self.converted_file_name[13:] + TextParseESTG.ENTER)
            aux = [".inputs "]
            for input_signal in self.inputs:
                aux.extend([" ", input_signal, " *"])
            aux_string = "".join(aux)
            f.write(aux_string + TextParseESTG.ENTER)
            aux = [".outputs "]
            for output_signal in self.outputs:
                aux.extend([" ", output_signal, " *"])
            aux_string = "".join(aux)
            f.write(aux_string + TextParseESTG.ENTER)
            for place in self.initial_places_list:
                if place not in traversed_places:
                    self.__recursive_transition_write(f, place, concurrency_close_map, traversed_places)
            aux = ".start "
            for index, place in enumerate(self.initial_places_list):
                if index == 0:
                    aux += place
                else:
                    aux += " " + place
            f.write(aux + TextParseESTG.ENTER)
            f.write(".end")

    def __recursive_transition_write(self, file, current_place, concurrency_close_map, traversed_places):
        traversed_places[current_place] = 1
        for transition in self.extended_graph[current_place]:
            if transition in self.node_classification:
                if self.node_classification[transition][0] == ESTGGraph.CONCURRENCY_OPEN:
                    aux = current_place + "/"
                    for index, place in enumerate(self.extended_graph[transition]):
                        if index == 0:
                            aux += place
                        else:
                            aux += "," + place
                    file.write(aux + "|" + TextParseSTG.__get_pure_transition(transition) + TextParseESTG.ENTER)
                    for place in self.extended_graph[transition]:
                        if place not in traversed_places:
                            self.__recursive_transition_write(file, place, concurrency_close_map, traversed_places)
                elif self.node_classification[transition][0] == ESTGGraph.CONCURRENCY_CLOSE_OR_HUB:
                    if transition not in concurrency_close_map:
                        concurrency_close_map[transition] = [[current_place],
                                                             self.node_classification[transition][1] - 1]
                        for place in self.extended_graph[transition]:
                            if place not in traversed_places:
                                self.__recursive_transition_write(file, place, concurrency_close_map, traversed_places)
                    elif concurrency_close_map[transition][1] != 1:
                        concurrency_close_map[transition][0].append(current_place)
                        concurrency_close_map[transition][1] -= 1
                    elif concurrency_close_map[transition][1] == 1:
                        aux = current_place
                        for place in concurrency_close_map[transition][0]:
                            aux += "," + place
                        aux += "/"
                        for index, place in enumerate(self.extended_graph[transition]):
                            if index == 0:
                                aux += place
                            else:
                                aux += "," + place
                        file.write(aux + "|" + TextParseSTG.__get_pure_transition(transition) + TextParseESTG.ENTER)

            else:
                aux = current_place + "/" + self.extended_graph[transition][0] + "|" +\
                      TextParseSTG.__get_pure_transition(transition)
                file.write(aux + TextParseESTG.ENTER)
                if self.extended_graph[transition][0] not in traversed_places:
                    self.__recursive_transition_write(file, self.extended_graph[transition][0], concurrency_close_map,
                                                      traversed_places)

    @staticmethod
    def __get_pure_transition(transition):
        if re.match(r"\s*\w+[+-](/[0-9]+)", transition):
            return transition.split("/")[0]
        return transition
