from Bio import SwissProt

def parse(raw):
    protParse = SwissProt.read(raw)
    return protParse

def parse_biolib_db(path) -> object:
    with open(path) as f:
        lines = f.read().split('\n')
