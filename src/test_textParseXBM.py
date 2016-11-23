from unittest import TestCase
from textparsexbm import TextParseXBM
from textparseestg import TextParseESTG
import time
from estggraph import ESTGGraph
from directmapping import DirectMapping
from vhdlgenerator import VHDLGenerator


class TestTextParseXBM(TestCase):

    PATH_TO_TESTS = "../testFiles/"

    def test___init__(self):
        file_name = ["sbuf-send-pkt2-vf.txt", "ALU2-vf.txt", "biu-dma2fifo-VF.txt",
                     "biu-fifo2dma-VF.txt", "des-vf.txt", "isqrt-vf.txt", "scsi-init-send-vf.txt",
                     "scsi-targ-send-vf.txt", "select2p-vf.txt", "selmerge2ph-vf.txt"]
        # file_name = ["select2p-vf.txt"]
        for f in file_name:
            text_parse = TextParseXBM(f)

    def test_gaga(self):
        file = ["testFile", "sbuf-send-pkt2-vf", "ALU2-vf", "biu-dma2fifo-VF", "biu-fifo2dma-VF", "des-vf",
                "isqrt-vf", "scsi-init-send-vf", "scsi-targ-send-vf", "select2p-vf", "selmerge2ph-vf", "I2C"]
        # file = ["alloc-outbound", "chu172", "atod", "ebergen", "master-read", "ram-read-sbuf", "sbuf-ram-write",
        #         "sendr-done"]
        for f in file:
            averager = 0
            print(f)
            for i in range(1000):
                a = time.clock()
                parse_test = TextParseESTG(self.PATH_TO_TESTS + f)
                parse_test.read_file()
                estg_graph = ESTGGraph(parse_test)
                # estg_graph.check_consistency()
                estg_graph.check_output_persistency()
                direct = DirectMapping(estg_graph)
                generator = VHDLGenerator(direct, f, False)
                b = time.clock()
                averager += (b-a)
            print("Time elapsed: " + str(averager/1000))
            tran = 0
            place = 0
            for node in estg_graph.extended_graph.keys():
                if node.is_place:
                    place += 1
                else:
                    tran += 1
            print("Places/Tran: " + str(place) + "/" + str(tran))
            output = 0
            inputy = 0
            for signal in estg_graph.signal_map.keys():
                if estg_graph.signal_map[signal] == ESTGGraph.OUTPUT:
                    output += 1
                else:
                    inputy += 1
            print("Input/Output: " + str(inputy) + "/" + str(output))

    def test_gaga2(self):
        file = ["testFile", "sbuf-send-pkt2-vf", "ALU2-vf", "biu-dma2fifo-VF", "biu-fifo2dma-VF", "des-vf",
                "isqrt-vf", "scsi-init-send-vf", "scsi-targ-send-vf", "select2p-vf", "selmerge2ph-vf", "I2C"]
        file = ["chu172"]
        for f in file:
            print(f)
            parse_test = TextParseESTG(self.PATH_TO_TESTS + f)
            parse_test.read_file()
            estg_graph = ESTGGraph(parse_test)
            # estg_graph.check_consistency()
            estg_graph.check_output_persistency()
            direct = DirectMapping(estg_graph)
            generator = VHDLGenerator(direct, f, False)
