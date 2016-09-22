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
        initial_place_list = []
        node_classification = {}
        if converted_file_name == "":
            if re.match(r"^.+\.g$", file_to_convert):
                converted_file_name = file_to_convert[:-2]
            else:
                raise Exception("Give a file name for the output or choose a file with compatible extension!")
        if os.path.isfile(path_to_descriptions + converted_file_name):
            answer = input(converted_file_name + "file already exist. Do you want to ovewrite it?(s/n)")
            if answer != "s":
                raise FileExistsError("File already exist!")
        if os.path.isfile(path_to_descriptions + converted_file_name) and not GraphUtil.__was_file_changed(
                converted_file_name):
            return
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
        extended_graph, initial_place_list = GraphUtil.__get_extended_graph(initial_markings, graph)
        GraphUtil.__classify_nodes(extended_graph, node_classification)
        GraphUtil.__write_file(name, inputs, outputs, extended_graph, node_classification, converted_file_name, initial_place_list)
        return inputs, outputs, graph, name, initial_markings, extended_graph, node_classification

    @staticmethod
    def __write_file(name, inputs, outputs, extended_graph, node_classification, converted_file_name, initial_places):
        path_to_descriptions = "../testFiles/"
        enter = "\n"
        traversed_places = {}
        concurrency_close_map = {}
        with open(path_to_descriptions + converted_file_name, 'w') as f:
            if name != "":
                f.write(".name " + name + enter)
            aux = [".inputs "]
            for input_signal in inputs:
                aux.extend([" ", input_signal, " *"])
            aux_string = "".join(aux)
            f.write(aux_string + enter)
            aux = [".outputs "]
            for output_signal in outputs:
                aux.extend([" ", output_signal, " *"])
            aux_string = "".join(aux)
            f.write(aux_string + enter)
            for place in initial_places:
                GraphUtil.__recursive_transition_write(f, extended_graph, node_classification, place,
                                                       concurrency_close_map, traversed_places)
            aux = ".start "
            for index, place in enumerate(initial_places):
                if index == 0:
                    aux += place
                else:
                    aux += " " + place
            f.write(aux + enter)
            f.write(".end")


    @staticmethod
    def __recursive_transition_write(file, extended_graph, node_classification, current_place, concurrency_close_map,
                                     traversed_places):
        enter = "\n"
        traversed_places[current_place] = 1
        for transition in extended_graph[current_place]:
            if transition in node_classification:
                if node_classification[transition][0] == ESTGGraph.CONCURRENCY_OPEN:
                    aux = current_place + "/"
                    for index, place in enumerate(extended_graph[transition]):
                        if index == 0:
                            aux += place
                        else:
                            aux += "," + place
                    file.write(aux + "|" + transition + enter)
                    for place in extended_graph[transition]:
                        if place not in traversed_places:
                            GraphUtil.__recursive_transition_write(file, extended_graph, node_classification, place,
                                                                   concurrency_close_map, traversed_places)
                elif node_classification[transition][0] == ESTGGraph.CONCURRENCY_CLOSE:
                    if transition not in concurrency_close_map:
                        concurrency_close_map[transition] = ([current_place], node_classification[transition][1] - 1)
                    elif concurrency_close_map[transition][1] == 1:
                        aux = current_place
                        for place in concurrency_close_map[transition][0]:
                            aux += "," + place
                        aux += "/"
                        for index, place in enumerate(extended_graph[transition]):
                            if index == 0:
                                aux += place
                            else:
                                aux += "," + place
                        file.write(aux + "|" + transition + enter)
                        for place in extended_graph[transition]:
                            if place not in traversed_places:
                                GraphUtil.__recursive_transition_write(file, extended_graph, node_classification, place,
                                                                       concurrency_close_map, traversed_places)
            else:
                aux = current_place + "/" + extended_graph[transition][0] + "|" + transition
                file.write(aux + enter)
                if extended_graph[transition][0] not in traversed_places:
                    GraphUtil.__recursive_transition_write(file, extended_graph, node_classification,
                                                           extended_graph[transition][0], concurrency_close_map,
                                                           traversed_places)

    @staticmethod
    def __get_extended_graph(initial_markings, graph):
        extended_graph = {}
        place_relation = {}
        initial_transitions = []
        node_classification = {}
        place_count = [1]
        initial_places_list = []
        initial_places_flag = False
        if re.match(r"\w+[+-](\/[0-9]+)?", initial_markings):
            initial_transitions.append(initial_markings)
            initial_places_list.append(GraphUtil.__get_place_name(place_count))
            initial_places_flag = True
        elif GraphUtil.__is_place(initial_markings):
            place_relation[initial_markings] = GraphUtil.__get_place_name(place_count)
            initial_transitions = graph[initial_markings]
            extended_graph[GraphUtil.__get_place_name(place_count)] = initial_transitions
            initial_places_list.append(GraphUtil.__get_place_name(place_count))
            initial_places_flag = True
            place_count[0] += 1
        else:
            # Assumption that we have only one place or several transitions
            # TODO treat the case when we have places and transitions in here. Not that hard.
            aux_markings = set()
            transitions = initial_markings.split()
            for transition in transitions:
                aux_markings.add(transition.strip("<> ").split(',')[0])
            initial_transitions = list(aux_markings)
        for transition in initial_transitions:
            for following_node in graph[transition]:
                if GraphUtil.__is_place(following_node):
                    if not initial_places_flag:
                        initial_places_list.append(GraphUtil.__get_place_name(place_count))
                    place_relation[following_node] = GraphUtil.__get_place_name(place_count)
                    GraphUtil.__add_connection(extended_graph, transition, GraphUtil.__get_place_name(place_count))
                    place_count[0] += 1
                    GraphUtil.__aux_get_extended_graph(following_node, extended_graph, graph, place_count,
                                                       node_classification, place_relation)
                else:
                    if not initial_places_flag:
                        initial_places_list.append(GraphUtil.__get_place_name(place_count))
                    GraphUtil.__add_connection(extended_graph, transition, GraphUtil.__get_place_name(place_count))
                    GraphUtil.__add_connection(extended_graph, following_node, GraphUtil.__get_place_name(place_count),
                                               False)
                    place_count[0] += 1
                    GraphUtil.__aux_get_extended_graph(following_node, extended_graph, graph, place_count,
                                                       node_classification, place_relation)

        return extended_graph, initial_places_list

    @staticmethod
    def __aux_get_extended_graph(current_node, extended_graph, graph, place_count, node_classification, place_relation):
        if GraphUtil.__is_place(current_node):
            for transition in graph[current_node]:
                GraphUtil.__add_connection(extended_graph, transition, current_node, False)
                if transition in extended_graph:
                    continue
                else:
                    GraphUtil.__aux_get_extended_graph(transition, extended_graph, graph, place_count,
                                                       node_classification, place_relation)
        else:
            for node in graph[current_node]:
                if GraphUtil.__is_place(node):
                    if node in place_relation:
                        GraphUtil.__add_connection(extended_graph, current_node, node)
                        continue
                    else:
                        place_relation[node] = GraphUtil.__get_place_name(place_count)
                        GraphUtil.__add_connection(extended_graph, current_node,
                                                   GraphUtil.__get_place_name(place_count))
                        place_count[0] += 1
                        GraphUtil.__aux_get_extended_graph(node, extended_graph, graph, place_count,
                                                           node_classification, place_relation)
                else:
                    GraphUtil.__add_connection(extended_graph, current_node, GraphUtil.__get_place_name(place_count))
                    GraphUtil.__add_connection(extended_graph, node, GraphUtil.__get_place_name(place_count), False)
                    place_count[0] += 1
                    if node in extended_graph:
                        continue
                    else:
                        GraphUtil.__aux_get_extended_graph(node, extended_graph, graph, place_count,
                                                           node_classification, place_relation)

    @staticmethod
    def __classify_nodes(extended_graph, node_classification):
        transition_fanin_count = {}
        for node in extended_graph.keys():
            if GraphUtil.__is_place(node):
                if len(extended_graph[node]) > 1:
                    node_classification[node] = (ESTGGraph.CHOICE_OPEN, len(extended_graph[node]))
                for transition in extended_graph[node]:
                    if transition not in transition_fanin_count:
                        transition_fanin_count[transition] = 1
                    else:
                        transition_fanin_count[transition] += 1
            else:
                if len(extended_graph[node]) > 1:
                    node_classification[node] = (ESTGGraph.CONCURRENCY_OPEN, len(extended_graph[node]))
        for transition in transition_fanin_count:
            if transition_fanin_count[transition] > 1:
                node_classification[transition] = (ESTGGraph.CONCURRENCY_CLOSE, transition_fanin_count[transition])


    @staticmethod
    def __add_connection(extended_graph, transition, place, is_transition_parent=True):
        if is_transition_parent:
            if transition not in extended_graph:
                extended_graph[transition] = [place]
            else:
                extended_graph[transition].append(place)
        else:
            if place not in extended_graph:
                extended_graph[place] = [transition]
            else:
                extended_graph[place].append(transition)

    @staticmethod
    def __get_place_name(place_count):
        return "place" + str(place_count[0])

    @staticmethod
    def __is_place(node):
        if re.match(r"\w+$", node):
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
        if os.path.isfile(path_to_graph + file_name) and not GraphUtil.__was_file_changed(file_name):
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
    def __was_file_changed(file_name):
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




