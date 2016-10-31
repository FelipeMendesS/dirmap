import graphviz as gv
import os
import pickle
import hashlib
from typing import Tuple
from estggraph import ESTGGraph
from textparseestg import TextParseESTG
Transition = Tuple[str, str]


class GraphUtil(object):

    @staticmethod
    def print_graph(graph: ESTGGraph, file_name: str, view_flag: bool=False, overwrite_graph: bool=False):
        if os.path.isfile(TextParseESTG.PATH_TO_GRAPH + file_name) and not GraphUtil.__was_file_changed(file_name)\
                and not overwrite_graph:
            if view_flag:
                gv.view(TextParseESTG.PATH_TO_GRAPH + file_name + TextParseESTG.SVG_EXTENSION)
            return
        g = gv.Digraph(format='svg', strict=True)
        initial_marking = graph.initial_places
        mark_traversed_transitions = {}
        mark_placed_places = {}
        for place in initial_marking:
            if place not in mark_placed_places:
                g.node(place.name, shape="circle", width=".5", fixedsize="true")
                mark_placed_places[place] = 1
            for end_place in graph.stg_graph[place]:
                if end_place not in mark_placed_places:
                    g.node(end_place.name, shape="circle", width=".5", fixedsize="true")
                    mark_placed_places[end_place] = 1
                key = place.name + end_place.name + str(graph.stg_graph_transitions[(place, end_place)])
                if key not in mark_traversed_transitions:
                    transition = graph.stg_graph_transitions[(place, end_place)]
                    g.node(transition.name, label="",
                           xlabel=GraphUtil.__transition_to_string(transition.transition),
                           shape="box", width="0.5", height="0.001")
                    g.edge(place.name, transition.name, arrowhead="onormal", arrowsize="0.5")
                    g.edge(transition.name, end_place.name)
                    mark_traversed_transitions[key] = 1
                GraphUtil.__aux_print_graph(mark_traversed_transitions, mark_placed_places, g, end_place, graph)
        g.render(TextParseESTG.PATH_TO_GRAPH + file_name)
        g.save(TextParseESTG.PATH_TO_GRAPH + file_name)
        if view_flag:
            gv.view(TextParseESTG.PATH_TO_GRAPH + file_name + TextParseESTG.SVG_EXTENSION)

    @staticmethod
    def is_free_choice_stg(graph: ESTGGraph):
        for place in graph.stg_graph.keys():
            if len(graph.extended_graph[place]) > 1:
                base_set_of_places = set(graph.inverted_extended_graph[graph.extended_graph[place][0]])
                for transition in graph.extended_graph[place]:
                    comparative_set_of_places = set(graph.inverted_extended_graph[transition])
                    if comparative_set_of_places != base_set_of_places:
                        return False
        return True


    @staticmethod
    def __aux_print_graph(traversed_transitions: dict, traversed_places: dict, g: gv.Digraph, marking,
                          graph: ESTGGraph):
        for end_place in graph.stg_graph[marking]:
            if end_place not in traversed_places:
                g.node(end_place.name, shape="circle", width=".5", fixedsize="true")
                traversed_places[end_place] = 1
            elif end_place in traversed_places:
                key = marking.name + end_place.name + str(graph.stg_graph_transitions[(marking,  end_place)])
                if key not in traversed_transitions:
                    transition = graph.stg_graph_transitions[(marking, end_place)]
                    g.node(transition.name, label="",
                           xlabel=GraphUtil.__transition_to_string(transition.transition),
                           shape="box", width="0.5", height="0.01")
                    g.edge(marking.name, transition.name, arrowhead="onormal", arrowsize="0.5")
                    g.edge(transition.name, end_place.name)
                    traversed_transitions[key] = 1
                continue
            key = marking.name + end_place.name + str(graph.stg_graph_transitions[(marking, end_place)])
            if key not in traversed_transitions:
                transition = graph.stg_graph_transitions[(marking, end_place)]
                g.node(transition.name, label="",
                       xlabel=GraphUtil.__transition_to_string(transition.transition),
                       shape="box", width="0.5", height="0.01")
                g.edge(marking.name, transition.name, arrowhead="onormal", arrowsize="0.5")
                g.edge(transition.name, end_place.name)
                traversed_transitions[key] = 1
            GraphUtil.__aux_print_graph(traversed_transitions, traversed_places, g, end_place, graph)
    # Only renders the svg file if it doesn't exist yet or if the description was changed after the last time.

    @staticmethod
    def __transition_to_string(transition):
        transition_string = ""
        for signal, transition_type in transition:
            aux = ESTGGraph.SYMBOL_DICT[transition_type]
            transition_string = transition_string + aux[0] + signal + aux[1]
        return transition_string

    @staticmethod
    def __was_file_changed(file_name):
        # Used as reference in
        # http://stackoverflow.com/questions/1912567/python-library-to-detect-if-a-file-has-changed-between-different-runs
        try:
            data = pickle.load(open("fileState", 'rb'))
        except (EOFError, FileNotFoundError, IOError):
            data = []
        last_state = dict(data)
        checksum = hashlib.md5(open(TextParseESTG.PATH_TO_DESCRIPTIONS + file_name).read().encode('utf-8')).hexdigest()
        if file_name not in last_state or last_state[file_name] != checksum:
            last_state[file_name] = checksum
            pickle.dump(list(last_state.items()), open("fileState", "wb"))
            return True
        return False
