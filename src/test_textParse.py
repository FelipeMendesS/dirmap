from unittest import TestCase
from textparse import TextParse
from graphutil import GraphUtil
import graphviz as gv


class TestTextParse(TestCase):

    PATH_TO_TESTS = "../testFiles/"
    PATH_TO_IMAGES = "../graph/"

    def test_check_file(self):
        return

    def test_read_file1(self):
        file = "testFile"
        parse_test = TextParse(self.PATH_TO_TESTS + file)
        parse_test.read_file()
        GraphUtil.print_graph(parse_test.graph, file)
        parse_test.graph.check_consistency()
        parse_test.graph.check_output_persistency()
        self.assertEqual(parse_test.regular_inputs, ["req", "ackline"])
        self.assertEqual(parse_test.outputs, ["ack", "sendline"])
        # print(parse_test.graph.stg_graph)
        # print(parse_test.graph.initial_places)
        # print(parse_test.graph.extended_graph)
        # print(parse_test.graph.transitions_identification)
        # print(parse_test.graph.signal_map)
        # print(parse_test.graph.transition_variables)

    def test_read_file2(self):
        file = "testFile2"
        parse_test = TextParse(self.PATH_TO_TESTS + file)
        parse_test.read_file()
        GraphUtil.print_graph(parse_test.graph, file)
        parse_test.graph.check_consistency()
        parse_test.graph.check_output_persistency()
        self.assertEqual(parse_test.regular_inputs, ["ackin", "dack", "done", "dtc", "startdmasend"])
        self.assertEqual(parse_test.outputs, ["dreq", "endmaint", "ready", "regout"])

    def test_read_file3(self):
        file = "testFile3"
        parse_test = TextParse(self.PATH_TO_TESTS + file)
        parse_test.read_file()
        GraphUtil.print_graph(parse_test.graph, file)
        parse_test.graph.check_consistency()
        parse_test.graph.check_output_persistency()
        self.assertEqual(parse_test.regular_inputs, ["a", "d"])
        self.assertEqual(parse_test.outputs, ["b", "c", "x"])

    def test_read_file4(self):
        file = "testFile4"
        parse_test = TextParse(self.PATH_TO_TESTS + file)
        parse_test.read_file()
        GraphUtil.print_graph(parse_test.graph, file)
        parse_test.graph.check_consistency()
        parse_test.graph.check_output_persistency()
        self.assertEqual(parse_test.regular_inputs, ["a", "b"])
        self.assertEqual(parse_test.outputs, ["x", "y", "z"])

    def test_create_graph(self):
        return

    def test_stg_conversion(self):
        inputs, outputs, graph, name, initial_markings = GraphUtil.stg_to_estg(self.PATH_TO_TESTS + "alloc-outbound.g")
        print(graph)