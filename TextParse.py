import re


class TextParse (object):

    def __init__(self, input_file):
        with open(input_file, 'r') as f:
            self.file_lines = f.readlines()
        self.regular_inputs = []
        self.outputs = []
        self.choice_inputs = []
        self.especification_name = ""
        # self.initial_state = bitarray

    def check_file(self):
        # Check if file is correct with basic checks
        # Use all inputs, outputs and level signals declared and all transitions contain only declared inputs and outputs
        # Contains initial value and ending. (Warning if contain anything after ending
        # Warning if doesn't contain specification name
        a = self.file_lines
        return

    def read_file(self):
        # loop checking for each and all cases creating data structures with transitions, inputs, outputs and choices
        input = re.compile("\b\.inputs*")
        output = re.compile("\b\.outputs*")
        name = re.compile("\b\.name*")
        choice = re.compile("\b\.choice*")
        start = re.compile("\b\.start*")
        end = re.compile("\b\.end*")
        for line in self.file_lines:
            if input.match(line):
                return
            if output.match(line):
                return
            if name.match(line):
                return
            if choice.match(line):
                return
            if start.match(line):
                return
            if end.match(line):
                return
        return

    def create_graph(self):
        # Create STG graph from file
        a = self.file_lines
        return