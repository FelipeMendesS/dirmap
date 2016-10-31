import re
from typing import List, Dict, Union
from node import Node

class TextParseESTG (object):

    PATH_TO_DESCRIPTIONS = "../testFiles/"
    ENTER = "\n"
    PATH_TO_GRAPH = "../graph/"
    SVG_EXTENSION = ".svg"

    def __init__(self, input_file):
        with open(input_file, 'r') as f:
            self.file_lines = f.read().splitlines()
        self.regular_inputs = []  # type: List[str]
        self.outputs = []  # type: List[str]
        self.conditional_signals = []  # type: List[str]
        self.specification_name = ""  # type: str
        self.initial_places = []  # type: List[Node]
        # Map with: (Key: Name of variable, Value: Initial value)
        self.initial_signal_values = {}  # type: Dict[str, Union[int, str]]
        self.transitions = []  # type: List[str]

    def check_file(self):
        '''
        Checks if file follows some basic premisses. Most of the checks are made in the estggraph class
        Checks if file contains name and initial markings. If not, show some warnings.
        '''
        if self.specification_name == "":
            print("Warning: No name for this specification!")
        if len(self.initial_places) == 0:
            print("Warning: No initial places specified. This is necessary before synthesis!")

    def read_file(self):
        # loop checking for each and all cases creating data structures with transitions, inputs, outputs cond signals
        reached_end = 0
        aux_initial_places = []
        for index, line in enumerate(self.file_lines):
            if re.match(r"^\s*\.name\s+.+", line):
                self.specification_name = line.lstrip(' .name').strip()
            elif re.match(r"^\s*\.inputs(\s+\w+\s+[01*])+", line):
                aux = line.strip()[7:].split()
                for i in range(round(len(aux)/2)):
                    self.regular_inputs.append(aux[i * 2])
                    if not aux[i * 2 + 1] == "*":
                        self.initial_signal_values[aux[i * 2]] = int(aux[i * 2 + 1])
                    else:
                        self.initial_signal_values[aux[i * 2]] = aux[i * 2 + 1]
            elif re.match(r"^\s*\.outputs(\s+\w+\s+[01*])+", line):
                aux = line.strip()[8:].split()
                for i in range(round(len(aux)/2)):
                    self.outputs.append(aux[i * 2])
                    if not aux[i * 2 + 1] == "*":
                        self.initial_signal_values[aux[i * 2]] = int(aux[i * 2 + 1])
                    else:
                        self.initial_signal_values[aux[i * 2]] = aux[i * 2 + 1]
            elif re.match(r"^\s*\.choice(\s+\w+\s+[01*])+", line):
                aux = line.strip()[7:].split()
                for i in range(round(len(aux)/2)):
                    self.conditional_signals.append(aux[i * 2])
                    self.initial_signal_values[aux[i * 2]] = int(aux[i * 2 + 1])
            elif re.match(r"^\s*\.start(\s+\w+)+", line):
                aux_initial_places.extend(line.strip()[6:].split())
            elif re.match(r"^\s*\.end\s*$", line):
                reached_end = 1
                if index < len(self.file_lines) - 1:
                    print("Warning! There are lines after the end statement. If these are relevant fix it!")
                break
            # Maybe add some flexibility for the spaces in these cases
            else:
                if re.match(r"\w+\s*(,\s*\w+\s*)*/\s*\w*\s*(,\s*\w+\s*)*\|\s*#?\w+[+\-*](\s*,\s*#?\w+[+\-*])*", line):
                    self.transitions.append(line)
                elif not re.match("^\s*#.*$", line):
                    raise Exception("Line not read: " + line)

        if reached_end == 0:
            raise Exception("No end statement")
        for place in aux_initial_places:
            self.initial_places.append(Node(True, place))
        self.check_file()
