import re
from estggraph import ESTGGraph


class TextParse (object):

    SIMPLE_TRANSITION = 0
    CONCURRENCY = 1
    DECISION = 2
    CONVERGENCE = 3

    def __init__(self, input_file):
        with open(input_file, 'r') as f:
            self.file_lines = f.read().splitlines()
        self.regular_inputs = []
        self.outputs = []
        self.choice_inputs = []
        self.specification_name = ""  # type: str
        self.initial_places = []
        # Map with: (Key: Name of variable, Value: Initial value)
        self.initial_signal_values = {}  # type: dict
        self.transitions = []
        self.graph = 0  # type: ESTGGraph

    def check_file(self):
        # Check if file is correct with basic checks
        # Use all inputs, outputs and level signals declared and all transitions contain only declared
        # inputs and outputs
        # Contains initial value and ending. (Warning if contain anything after ending
        # Warning if doesn't contain specification name
        # TODO: Include a check for the starting place, if it exhists (Easy)
        if self.specification_name == "":
            print("Warning: No name for this especification!")
        variable_check_map = dict.fromkeys(self.graph.signal_map.keys(), 0)
        for value in self.graph.transition_variables.values():
            for variable in value[0]:
                if variable in variable_check_map:
                    variable_check_map[variable] = 1
                else:
                    raise Exception("Variable not declared: " + variable)
        for key, value in variable_check_map.items():
            if value != 1:
                print("Warning! Variable", key, "declared but not used.")

    def read_file(self):
        # loop checking for each and all cases creating data structures with transitions, inputs, outputs and choices
        reached_end = 0
        for line in self.file_lines:
            if re.match(r"^\s*\.name\s+.+", line):
                self.specification_name = line.lstrip(' .name').strip()
            elif re.match(r"^\s*\.inputs(\s+\w+\s+[01*])+", line):
                aux = line.strip()[7:].split()
                for i in range(round(len(aux)/2)):
                    self.regular_inputs.append(aux[i * 2])
                    self.initial_signal_values[aux[i * 2]] = int(aux[i * 2 + 1])
            elif re.match(r"^\s*\.outputs(\s+\w+\s+[01*])+", line):
                aux = line.strip()[8:].split()
                for i in range(round(len(aux)/2)):
                    self.outputs.append(aux[i * 2])
                    self.initial_signal_values[aux[i * 2]] = int(aux[i * 2 + 1])
            elif re.match(r"^\s*\.choice(\s+\w+\s+[01*])+", line):
                aux = line.strip()[7:].split()
                for i in range(round(len(aux)/2)):
                    self.choice_inputs.append(aux[i * 2])
                    self.initial_signal_values[aux[i * 2]] = int(aux[i * 2 + 1])
            elif re.match(r"^\s*\.start(\s+\w+)+", line):
                self.initial_places.extend(line.strip()[6:].split())
            elif re.match(r"^\s*\.end\s*$", line):
                reached_end = 1
                # TODO Check if there are other lines after ending, to warn user
                break
            # Maybe add some flexibility for the spaces in these cases
            else:
                if re.match(r"\w+\s*/\s*\w+\s*\|\s*\w+[+\-*](\s*,\s*\w+[+\-*])*", line):
                    self.transitions.append((line, self.SIMPLE_TRANSITION))
                elif re.match(r"\w+\s*/\s*\w+(\s*,\s*\w+)+\s*\|\s*\w+[+\-*](\s*,\s*\w+[+\-*])*", line):
                    self.transitions.append((line, self.CONCURRENCY))
                elif re.match(r"\w+\s*,\s*\w+\s*/\s*\w+\s*\|\s*\w+[+\-*](\s*,\s*\w+[+\-*])*", line):
                    self.transitions.append((line, self.CONVERGENCE))
                elif re.match(r"\w+\s*/\s*\w+\s*\|\s*#\w+[+\-*](\s*,\s*\w+[+\-*])*", line):
                    self.transitions.append((line, self.DECISION))
        if reached_end == 0:
            raise Exception("No end statement")
        self.create_graph()
        self.check_file()

    def create_graph(self):
        # Create STG graph from file
        # Maybe change where the processing is made to make it a little bit cleaner
        self.graph = ESTGGraph(self.regular_inputs, self.outputs, self.choice_inputs, self.transitions,
                               self.initial_places, self.initial_signal_values)
        return
