from directmapping import DirectMapping
from estggraph import ESTGGraph
from textparseestg import TextParseESTG
from graphutil import GraphUtil
from vhdlgenerator import VHDLGenerator
import sys

PATH_TO_TESTS = "../testFiles/"
PATH_TO_IMAGES = "../graph/"

# In the future make the tool a little bit more robust but for now is enough.
# When writing the thesis, whenever I'm tired try to improve the tool!


def main():
    file_name = sys.argv[1]
    view_flag = False
    if len(sys.argv) > 2:
        view_flag = True
    parse_file = TextParseESTG(PATH_TO_TESTS + file_name)
    parse_file.read_file()
    estg_graph = ESTGGraph(parse_file)
    #estg_graph.check_consistency()
    #estg_graph.check_output_persistency()
    direct = DirectMapping(estg_graph)
    GraphUtil.print_graph(estg_graph, file_name, view_flag=view_flag, overwrite_graph=False)
    generator = VHDLGenerator(direct, file_name, False)
    print(generator.last_cycle_2_control_cell)

# Parse files and get them to directmapping or something like that. Already showing how the program is supposed to be
# run
if __name__ == '__main__':
    main()
