import re
from STGGraph import STGGraph

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
        self.especification_name = ""
        self.initial_condition = ()
        self.transitions = []
        self.graph = STGGraph("")
        # self.initial_state = bitarray

    def check_file(self):
        # Check if file is correct with basic checks
        # Use all inputs, outputs and level signals declared and all transitions contain only declared inputs and outputs
        # Contains initial value and ending. (Warning if contain anything after ending
        # Warning if doesn't contain specification name
        if self.especification_name == "":
            print "Warning: No name for this especification!"
        variable_check_map = dict.fromkeys(self.graph.variable_map.keys(), 0)
        for value in self.graph.transition_variables.values():
            for variable in value[0]:
                if variable in variable_check_map:
                    variable_check_map[variable] = 1
                else:
                    raise Exception("Variable not declared: ", variable)
        for key,value in variable_check_map.items():
            if value != 1:
                print "Warning! Variable", key, "declared but not used."

    def read_file(self):
        # loop checking for each and all cases creating data structures with transitions, inputs, outputs and choices
        reached_end = 0
        for line in self.file_lines:
            if re.match(r"^\s*\.name\s+.*", line):
                self.especification_name = line.lstrip(' .name')
            elif re.match(r"^\s*\.inputs\s+.*", line):
                self.regular_inputs.extend(line.lstrip(' .inputs ').split(' '))
                continue
            elif re.match(r"^\s*\.outputs\s+.*", line):
                self.outputs.extend(line.lstrip(' .outputs ').split(' '))
            elif re.match(r"^\s*\.choice\s+.*", line):
                self.choice_inputs.extend(line.lstrip(' .choice').split(' '))
            elif re.match(r"^\s*\.start\s+.*", line):
                self.initial_condition = line.lstrip(' .start').split('(')
                self.initial_condition[1] = re.match(r"\d*", self.initial_condition[1]).group().split()
                self.initial_condition = tuple(self.initial_condition)
            elif re.match(r"^\s*\.end\s*$", line):
                reached_end = 1
                # TODO Check if there are other lines after ending, to warn user
                break
            # Maybe add some flexibility for the spaces in these cases
            else:
                if re.match(r"\w+/\w+\|\w+[+\-*](,\w+[+\-*])*", line):
                    self.transitions.append((line, self.SIMPLE_TRANSITION))
                elif re.match(r"\w+/\w+,\w+\|\w+[+\-*](,\w+[+\-*])*", line):
                    self.transitions.append((line, self.CONCURRENCY))
                elif re.match(r"\w+,\w+/\w+\|\w+[+\-*](,\w+[+\-*])*", line):
                    self.transitions.append((line, self.CONVERGENCE))
                elif re.match(r"\w+/\w+\|#\w+[+\-*](,\w+[+\-*])*", line):
                    self.transitions.append((line, self.DECISION))
        if reached_end == 0:
            raise Exception("No end statement")
        self.create_graph()
        self.check_file()

    def create_graph(self):
        # Create STG graph from file
        self.graph = STGGraph(self)
        return
