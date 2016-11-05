from unittest import TestCase
from directmapping import DirectMapping
from textparseestg import TextParseESTG
from estggraph import ESTGGraph
from graphutil import GraphUtil
from vhdlgenerator import VHDLGenerator


class TestDirectMapping(TestCase):

    PATH_TO_TESTS = "../testFiles/"
    PATH_TO_IMAGES = "../graph/"

    def setUp(self):
        self.file = ["I2C"]
        for file in self.file:
            self.parse_test = TextParseESTG(self.PATH_TO_TESTS + file)
            self.parse_test.read_file()
            self.estg_graph = ESTGGraph(self.parse_test)
            self.direct = DirectMapping(self.estg_graph)
            self.generator = VHDLGenerator(self.direct, file, False)

        # GraphUtil.print_graph(self.estg_graph, file)


    # How to make this tests automated? Seems to be something pretty hard to automatically test without using the same
    # algorithm being tested to generate the results to be compared with
    # Improve testing!!! I just need some working tests before finishing these stuff.
    def test_get_set_of_control_cell_places(self):
        print("Set of control cell places")
        print(self.direct.set_of_control_cell_places)
        print("Control Cell graph")
        print(self.direct.control_cells_graph)
        print(self.direct.inverse_control_cells_graph)
        print("Places Trees")
        print(self.direct.logic_tree)
        print("3")
        print(self.direct.size_3_cycles)
        print("2")
        print(self.direct.size_2_cycles)
        print("1")
        print(self.direct.size_1_cycles)
        print("0")
        print(self.direct.cycle_0_final_transition)

    def test_check_for_size_2_cycles(self):
        print("Size 2 cycle")
        print(self.direct.size_2_cycles)
        print("Why")
        print(self.direct.cycle_0_final_transition)
        print("Control cell graph")
        print(self.direct.control_cells_graph)

    def test_input_connections(self):
        print("Inverse control cell graph")
        print(self.direct.inverse_control_cells_graph)
        print("Input to cell")

    def test_output_signal_values(self):
        print("Output value for each cell")
        print(self.direct.output_control_cell_relation)