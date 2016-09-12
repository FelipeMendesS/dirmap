import TextParse as tp


class TextParseTest(object):

    @staticmethod
    def testReadFile():
        parse_test = tp.TextParse("testFile")
        parse_test.read_file()
        print parse_test.regular_inputs, parse_test.outputs, parse_test.choice_inputs
        print parse_test.especification_name, parse_test.initial_condition
        print parse_test.transitions
        return

TextParseTest.testReadFile()
