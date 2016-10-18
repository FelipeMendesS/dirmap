from unittest import TestCase
from directmapping import DirectMapping
from textparseestg import TextParseESTG
from estggraph import ESTGGraph
from graphutil import GraphUtil


class TestDirectMapping(TestCase):

    PATH_TO_TESTS = "../testFiles/"
    PATH_TO_IMAGES = "../graph/"

    # How to make this tests automated? Seems to be something pretty hard to automatically test without using the same
    # algorithm being tested to generate the results to be compared with
    def test_get_set_of_control_cell_places(self):
        file = "pe-send-ifc"
        parse_test = TextParseESTG(self.PATH_TO_TESTS + file)
        parse_test.read_file()
        GraphUtil.print_graph(parse_test.graph, file, True)
        direct = DirectMapping(parse_test.graph)
        print(direct.set_of_control_cell_places)

    def test_check_for_size_2_cycles(self):
        file = "pe-send-ifc"
        parse_test = TextParseESTG(self.PATH_TO_TESTS + file)
        parse_test.read_file()
        direct = DirectMapping(parse_test.graph)
        print(direct.size_2_cycles)
        print(direct.cycle_0_final_transition)
        print(direct.control_cells_graph)
