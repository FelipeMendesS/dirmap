import graphviz as gv
import re
import os
import pickle
import hashlib
from estggraph import ESTGGraph

class GraphUtil(object):

    # Places with names starting with p concatenated with a number, in order of creation
    # TODO Finish implementation of conversion method
    @staticmethod
    def stg_to_estg(file_to_convert, converted_file_name=""):
        path_to_descriptions = "../testFiles/"
        inputs = []
        outputs = []
        graph = {}
        extended_graph = {}
        name = ""
        # If not declared starts from the first transition.
        initial_markings = ""
        place_name = "place"
        with open(file_to_convert, 'r') as f:
            file_lines = f.read().splitlines()
        for line in file_lines:
            if re.match(r"^#.*", line):
                continue
            elif re.match(r"^\s*\.name\s+\w+", line):
                name += line.strip()[5:].strip()
            elif re.match(r"^\s*\.inputs(\s+\w+)+", line):
                inputs.extend(line.strip()[7:].split())
            elif re.match(r"^\s*\.outputs(\s+\w+)+", line):
                outputs.extend(line.strip()[8:].split())
            elif re.match(r"^\s*\.internal(\s+\w+)+", line):
                outputs.extend(line.strip()[9:].split())
            elif re.match(r"^\s*\.dummy(\s+\w+)+", line):
                outputs.extend(line.strip()[6:].split())
            elif re.match(r"\s*\w+[+-]?(\/[0-9]+)?(\s+\w+[+-]?(\/[0-9]+)?)+", line):
                aux = line.strip().split()
                source_transition = aux[0]
                if initial_markings == "":
                    initial_markings = source_transition
                aux = aux[1:]
                if source_transition not in graph:
                    graph[source_transition] = []
                for variable in aux:
                    graph[source_transition].append(variable)
            elif re.match(r"\s*\.marking\s+", line):
                initial_markings = line.strip(".marking {}")
        if converted_file_name == "":
            if re.match(r"^.+\.g$", file_to_convert):
                converted_file_name = file_to_convert[:-2]
            else:
                raise Exception("Give a file name for the output or choose a file with compatible extension!")
        if os.path.isfile(path_to_descriptions + converted_file_name):
            answer = input(converted_file_name + "file already exist. Do you want to ovewrite it?(s/n)")
            if answer != "s":
                raise FileExistsError("File already exist!")
        initial_transitions = []
        place_relation = {}
        place_count
        if re.match(r"\w+[+-](\/[0-9]+)?", initial_markings):
            initial_transitions.append(initial_markings)
        elif GraphUtil.__is_place(initial_markings):
            place_relation[initial_markings] =
        extended_graph = GraphUtil.__get_extended_graph(initial_markings, graph)
        return inputs, outputs, graph, name, initial_markings

    @staticmethod
    def __get_extended_graph(initial_markings, graph):
        place_name = "place"
        extended_graph = {}
        place_relation = {}
        initial_transitions = []
        place_count = 1
        if re.match(r"\w+[+-](\/[0-9]+)?", initial_markings):
            return
        return {}

    @staticmethod
    def __aux_get_extended_graph(current_node, extended_graph, graph, place_count):



    @staticmethod
    def __is_place(node):
        if re.match(r"\w+", node):
            return True
        return False

    @staticmethod
    def __transition_to_string(transition):
        transition_string = ""
        for index, signal in enumerate(transition[0]):
            aux = ESTGGraph.SYMBOL_DICT[transition[1][index]]
            transition_string = transition_string + aux[0] + signal + aux[1]
        return transition_string

    @staticmethod
    def __aux_print_graph(traversed_transitions: dict, traversed_places: dict, g: gv.Digraph, marking, graph: ESTGGraph):
        for end_place in graph.stg_graph[marking]:
            if marking not in traversed_places:
                g.node(end_place)
                traversed_places[marking] = 1
            elif end_place in traversed_places:
                continue
            key = marking + end_place + str(graph .transition_variables[marking + end_place])
            if key not in traversed_transitions:
                g.edge(marking, end_place,
                       GraphUtil.__transition_to_string(graph.transition_variables[marking + end_place]))
                traversed_transitions[key] = 1
            GraphUtil.__aux_print_graph(traversed_transitions, traversed_places, g, end_place, graph)

    # Only renders the svg file if it doesn't exist yet or if the description was changed after the last time.
    @staticmethod
    def print_graph(graph: ESTGGraph, file_name: str, view_flag: bool=False):
        path_to_graph = "../graph/"
        svg_extension = ".svg"
        if os.path.isfile(path_to_graph + file_name) and not GraphUtil.__was_estg_changed(file_name):
            if view_flag:
                gv.view(path_to_graph + file_name + svg_extension)
            return
        g = gv.Digraph(format='svg')
        initial_marking = graph.initial_places
        mark_traversed_transitions = {}
        mark_placed_places = {}
        for place in initial_marking:
            if place not in mark_placed_places:
                g.node(place)
                mark_placed_places[place] = 1
            for end_place in graph.stg_graph[place]:
                if place not in mark_placed_places:
                    g.node(end_place)
                    mark_placed_places[place] = 1
                key = place + end_place + str(graph .transition_variables[place + end_place])
                if key not in mark_traversed_transitions:
                    g.edge(place, end_place,
                           GraphUtil.__transition_to_string(graph.transition_variables[place + end_place]))
                    mark_traversed_transitions[key] = 1
                GraphUtil.__aux_print_graph(mark_traversed_transitions, mark_placed_places, g, end_place, graph)
        g.render(path_to_graph + file_name)
        if view_flag:
            g.view(path_to_graph + file_name + svg_extension)

    @staticmethod
    def __was_estg_changed(file_name):
        path_to_descriptions = "../testFiles/"
        # Used as reference in
        # http://stackoverflow.com/questions/1912567/python-library-to-detect-if-a-file-has-changed-between-different-runs
        try:
            data = pickle.load(open("fileState", 'rb'))
        except (EOFError, FileNotFoundError, IOError):
            data = []
        last_state = dict(data)
        checksum = hashlib.md5(open(path_to_descriptions + file_name).read().encode('utf-8')).hexdigest()
        if file_name not in last_state or last_state[file_name] != checksum:
            last_state[file_name] = checksum
            pickle.dump(list(last_state.items()), open("fileState", "wb"))
            return True
        return False




