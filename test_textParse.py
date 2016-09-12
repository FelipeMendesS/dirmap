from unittest import TestCase
from TextParse import TextParse


class TestTextParse(TestCase):
    def test_check_file(self):
        return

    def test_read_file1(self):
        parse_test = TextParse("testFile")
        parse_test.read_file()
        self.assertEqual(parse_test.regular_inputs, ["req", "ackline"])
        self.assertEqual(parse_test.outputs, ["ack", "sendline"])
        return

    def test_read_file2(self):
        parse_test = TextParse("testFile2")
        parse_test.read_file()
        self.assertEqual(parse_test.regular_inputs, ["ackin", "dack", "done", "dtc", "startdmasend"])
        return

    def test_create_graph(self):
        return
