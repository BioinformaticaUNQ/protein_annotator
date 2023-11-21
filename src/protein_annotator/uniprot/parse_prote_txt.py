from Bio import SwissProt

def parse(raw):
    protParse = SwissProt.read(raw)
    return protParse