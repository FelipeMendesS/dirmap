from typing import Dict, List
import re


class TextParseXBM(object):

    PATH_TO_XBM = "../benchmarksxbmartigo/"
    PATH_TO_FILES = "../testFiles/"
    ENTER = "\n"
    PLACE = "p"

    def __init__(self, file_name):
        self.graph = {}  # type: Dict[str, List[str]]
        self.index_counter = {}
        with open(self.PATH_TO_XBM + file_name, 'r') as f:
            file_lines = f.read().splitlines()
        with open(self.PATH_TO_FILES + file_name[:-4], 'w+') as f:
            f.write(".name " + file_name[:-4] + self.ENTER)
            f.write(".inputs")
            output_flag = False
            transition_lines = []
            for line in file_lines:
                if re.match(r"\s*input\s*\w+\s*\w\s*", line):
                    aux = line.strip().split()
                    f.write(" " + aux[1] + " " + aux[2])
                elif re.match(r"\s*output\s*\w+\s*\w\s*", line):
                    if not output_flag:
                        f.write(self.ENTER)
                        f.write(".outputs")
                        output_flag = True
                    aux = line.strip().split()
                    f.write(" " + aux[1] + " " + aux[2])
                elif re.match(r"\s*\w+\s*\w+\s*[\[?\w\s*+\-\]?]+\|[\w\s*+\-]?", line):
                    transition_lines.append(line)
                    aux = line.strip().split()
                    if aux[0] in self.graph:
                        self.graph[aux[0]].append(aux[1])
                    else:
                        self.graph[aux[0]] = [aux[1]]
            f.write(self.ENTER)
            number_of_nodes = 0
            for integer in self.graph.keys():
                if int(integer) > number_of_nodes:
                    number_of_nodes = int(integer)
            number_of_nodes += 1
            counter = 1
            for integer in self.graph.keys():
                if len(self.graph[integer]) > 1:
                    self.index_counter[integer] = [0, len(self.graph[integer])]
                    list_places = list()
                    list_places.append(int(integer) * 2 + 2)
                    for i in range(len(self.graph[integer]) - 1):
                        list_places.append(number_of_nodes * 2 + counter)
                        counter += 1
                    self.index_counter[integer].append(list_places)
            print(self.index_counter)
            print(self.graph)
            for line in transition_lines:
                aux = line.strip().split('|')
                input_v = aux[0].strip().split()
                output_v = aux[1].strip().split()
                continue_flag = False
                if len(output_v) == 0 or len(aux) == 1:
                    f.write(self.PLACE + str(int(input_v[0]) * 2 + 1) + '/' + self.PLACE +
                            str(int(input_v[1]) * 2 + 1) + "|")
                    continue_flag = True
                else:
                    if input_v[0] in self.index_counter:
                        f.write(self.PLACE + str(int(input_v[0]) * 2 + 1) + '/' + self.PLACE +
                                str(self.index_counter[input_v[0]][2][self.index_counter[input_v[0]][0]]) + "|")
                    else:
                        f.write(self.PLACE + str(int(input_v[0]) * 2 + 1) + '/' + self.PLACE + str(int(input_v[0]) * 2 + 2) + "|")
                for index, input_signal in enumerate(input_v[2:]):
                    if index > 0:
                        f.write(", ")
                    if re.match(r"\[\w+[*\-+]\]", input_signal):
                        input_signal = "#" + input_signal.strip("[]")
                    f.write(input_signal)
                f.write(self.ENTER)
                if continue_flag:
                    continue
                if input_v[0] in self.index_counter:
                    f.write(self.PLACE + str(self.index_counter[input_v[0]][2][self.index_counter[input_v[0]][0]]) +
                            '/' + self.PLACE + str(int(input_v[1]) * 2 + 1) + '|')
                    self.index_counter[input_v[0]][0] += 1
                else:
                    f.write(self.PLACE + str(int(input_v[0]) * 2 + 2) + '/' + self.PLACE + str(int(input_v[1]) * 2 + 1) + '|')
                for index, output_signal in enumerate(output_v):
                    if index > 0:
                        f.write(", ")
                    f.write(output_signal)
                f.write(self.ENTER)
            f.write(".start p1" + self.ENTER)
            f.write(".end")
