from unittest import TestCase
from textparsexbm import TextParseXBM


class TestTextParseXBM(TestCase):

    def test___init__(self):
        # file_name = ["sbuf-send-pkt2-vf.txt", "ALU2-vf.txt", "biu-dma2fifo-VF.txt",
        #              "biu-fifo2dma-VF.txt", "des-vf.txt", "isqrt-vf.txt", "scsi-init-send-vf.txt",
        #              "scsi-targ-send-vf.txt", "select2p-vf.txt", "selmerge2ph-vf.txt"]
        file_name = ["select2p-vf.txt"]
        for f in file_name:
            text_parse = TextParseXBM(f)
