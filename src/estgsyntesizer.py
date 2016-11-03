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
    parse_file = TextParseESTG(PATH_TO_TESTS + file_name)
    parse_file.read_file()
    estg_graph = ESTGGraph(parse_file)
    direct = DirectMapping(estg_graph)
    # GraphUtil.print_graph(estg_graph, file_name, True, overwrite_graph=True)
    VHDLGenerator(direct, file_name)

# Parse files and get them to directmapping or something like that. Already showing how the program is supposed to be
# run
if __name__ == '__main__':
    main()
