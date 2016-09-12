import re


class STGGraph (object):

    # Data that we need to use
    # Check if we can ave a choice to different concurrencies, at first won't be implemented. Can change data structures
    # if needed.

    INPUT = 0
    OUTPUT = 1
    CHOICE = 2
    RISING_EDGE = 3
    FALLING_EDGE = 4
    DONT_CARE = 5
    LEVEL_HIGH = 6
    LEVEL_LOW = 7

    def __init__(self, parsedText):
        # Map to relate all variables to type (Input, output, choice and don't care)
        self.variable_map = {}
        # Map that shows graph and each node has its type in a tuple associated with the value
        self.stg_graph = {}
        # Map that shows the variables involved in each and every transition in the graph. The keys are made by the
        # concatenation of the nodes names
        self.transition_variables = {}
        self.initial_condition = ()
        if parsedText == "":
            return
        for input in parsedText.regular_inputs:
            self.variable_map[input] = self.INPUT
        for output in parsedText.outputs:
            self.variable_map[output] = self.OUTPUT
        for choice in parsedText.choice_inputs:
            self.variable_map[choice] = self.CHOICE
        for line in parsedText.transitions:
            # Deal better with possible spaces in the input file
            [vertices, variables] = line[0].split('|')
            transition_type = line[1]
            v = []
            t = []
            for variable in variables.split(','):
                if re.match(r"#\w+[+\-*]", variable):
                    if variable[-1] == "+":
                        t.append(self.LEVEL_HIGH)
                    elif variable[-1] == "-":
                        t.append(self.LEVEL_LOW)
                    else:
                        t.append(self.DONT_CARE)
                else:
                    if variable[-1] == "+":
                        t.append(self.RISING_EDGE)
                    elif variable[-1] == "-":
                        t.append(self.FALLING_EDGE)
                    else:
                        t.append(self.DONT_CARE)
                v.append(variable.strip('#+-*'))
            transition_conditions = (v, t)
            [origin_vertex, destination_vertex] = vertices.split('/')
            for origin in origin_vertex.split(','):
                if not self.stg_graph.has_key(origin):
                    self.stg_graph[origin] = ([], 0)
                for destination in destination_vertex.split(','):
                    self.stg_graph[origin][0].append(destination)
                    self.stg_graph[origin] = (self.stg_graph[origin][0], transition_type)
                    self.transition_variables[origin + destination] = (v, t)

    def check_consistency(self):
        return

    def check_output_persistency(self):
        return