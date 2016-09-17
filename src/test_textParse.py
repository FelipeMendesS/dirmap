from unittest import TestCase
from textparse import TextParse


class TestTextParse(TestCase):

    PATH_TO_TESTS = "../testFiles/"

    def test_check_file(self):
        return

    def test_read_file1(self):
        parse_test = TextParse(self.PATH_TO_TESTS + "testFile")
        parse_test.read_file()
        parse_test.graph.check_consistency()
        self.assertEqual(parse_test.regular_inputs, ["req", "ackline"])
        self.assertEqual(parse_test.outputs, ["ack", "sendline"])
        # print(parse_test.graph.stg_graph)
        # print(parse_test.graph.initial_places)
        # print(parse_test.graph.extended_graph)
        # print(parse_test.graph.transitions_identification)
        # print(parse_test.graph.signal_map)
        # print(parse_test.graph.transition_variables)

    def test_read_file2(self):
        parse_test = TextParse(self.PATH_TO_TESTS + "testFile2")
        parse_test.read_file()
        parse_test.graph.check_consistency()
        self.assertEqual(parse_test.regular_inputs, ["ackin", "dack", "done", "dtc", "startdmasend"])
        self.assertEqual(parse_test.outputs, ["dreq", "endmaint", "ready", "regout"])

    def test_read_file3(self):
        parse_test = TextParse(self.PATH_TO_TESTS + "testFile3")
        parse_test.read_file()
        parse_test.graph.check_consistency()
        self.assertEqual(parse_test.regular_inputs, ["a", "d"])
        self.assertEqual(parse_test.outputs, ["b", "c", "x"])

    def test_read_file4(self):
        parse_test = TextParse(self.PATH_TO_TESTS + "testFile4")
        parse_test.read_file()
        parse_test.graph.check_consistency()
        self.assertEqual(parse_test.regular_inputs, ["a", "b"])
        self.assertEqual(parse_test.outputs, ["x", "y", "z"])

    def test_create_graph(self):
        return
