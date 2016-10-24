from unittest import TestCase
from textparseestg import TextParseESTG
from estggraph import ESTGGraph
from graphutil import GraphUtil
from textparsestg import TextParseSTG
import graphviz as gv
import traceback


class TestTextParse(TestCase):

    PATH_TO_TESTS = "../testFiles/"
    PATH_TO_IMAGES = "../graph/"

    def test_check_file(self):
        return

    def test_read_file1(self):
        file = "testFile"
        parse_test = TextParseESTG(self.PATH_TO_TESTS + file)
        parse_test.read_file()
        estg_graph = ESTGGraph(parse_test)
        GraphUtil.print_graph(estg_graph, file)
        estg_graph.check_consistency()
        estg_graph.check_output_persistency()
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
        parse_test = TextParseESTG(self.PATH_TO_TESTS + file)
        parse_test.read_file()
        estg_graph = ESTGGraph(parse_test)
        GraphUtil.print_graph(estg_graph, file)
        estg_graph.check_consistency()
        estg_graph.check_output_persistency()
        self.assertEqual(parse_test.regular_inputs, ["ackin", "dack", "done", "dtc", "startdmasend"])
        self.assertEqual(parse_test.outputs, ["dreq", "endmaint", "ready", "regout"])

    def test_read_file3(self):
        file = "testFile3"
        parse_test = TextParseESTG(self.PATH_TO_TESTS + file)
        parse_test.read_file()
        estg_graph = ESTGGraph(parse_test)
        GraphUtil.print_graph(estg_graph, file)
        estg_graph.check_consistency()
        estg_graph.check_output_persistency()
        self.assertEqual(parse_test.regular_inputs, ["a", "d"])
        self.assertEqual(parse_test.outputs, ["b", "c", "x"])

    def test_read_file4(self):
        file = "testFile4"
        parse_test = TextParseESTG(self.PATH_TO_TESTS + file)
        parse_test.read_file()
        estg_graph = ESTGGraph(parse_test)
        GraphUtil.print_graph(estg_graph, file)
        estg_graph.check_consistency()
        estg_graph.check_output_persistency()
        self.assertEqual(parse_test.regular_inputs, ["a", "b"])
        self.assertEqual(parse_test.outputs, ["x", "y", "z"])

    def test_create_graph(self):
        return

    def test_stg_conversion(self):
        # inputs, outputs, graph, name, initial_markings, extended_graph, node_classification =\
        # #     GraphUtil.stg_to_estg(self.PATH_TO_TESTS + "atod.g", overwrite_file_flag=False)
        # files = ["alloc-outbound", "atod", "chu172", "ebergen", "fifo", "hybridf", "master-read", "meng9",
        #          "pe-send-ifc", "qr42", "ram-read-sbuf", "rpdft", "sbuf-ram-write", "sendr-done", "sm", "trimos-send",
        #          "vbe10b", "wrdatab"]
        files = ["meng9"]
        extension = ".g"
        for file in files:
            try:
                print(file)
                stg_conversion = TextParseSTG(self.PATH_TO_TESTS + file + extension, overwrite_file_flag=True)
                parse_test = TextParseESTG(self.PATH_TO_TESTS + file)
                parse_test.read_file()
                estg_graph = ESTGGraph(parse_test)
                GraphUtil.print_graph(estg_graph, file, view_flag=True, overwrite_graph=True)
                print("Success")
            except Exception as e:
                traceback.print_exc()
        # print(graph)
        # print(extended_graph)
        # print(node_classification)

    def test_free_choice_test(self):
        files = ["alloc-outbound", "atod", "chu172", "ebergen", "fifo", "hybridf", "master-read", "meng9",
                 "pe-send-ifc", "qr42", "ram-read-sbuf", "rpdft", "sbuf-ram-write", "sendr-done", "sm", "trimos-send",
                 "vbe10b", "wrdatab"]
        for file in files:
            parse_test = TextParseESTG(self.PATH_TO_TESTS + file)
            parse_test.read_file()
            estg_graph = ESTGGraph(parse_test)
            if not GraphUtil.is_free_choice_stg(estg_graph):
                GraphUtil.print_graph(estg_graph, file, view_flag=True)
