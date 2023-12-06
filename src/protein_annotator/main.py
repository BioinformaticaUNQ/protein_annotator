

import pathlib
from protein_annotator.schemas import ProteinData
from protein_annotator.tools import file_exists, get_fasta_from_uniprot, is_fasta, is_uniprot_id, parse_fasta
class ProteinAnnotator:

    ##
    def __init__(self, input):
        self.protein_data = self.parse_input(input)
        
    def parse_sequence(self, input):
        pass

    def parse_input(self, input) -> ProteinData:
        if (is_fasta(input)):
            return parse_fasta(input)
        elif is_uniprot_id(input):
            return get_fasta_from_uniprot(input)
        else:
            raise Exception("Input provided must be a path to a fasta file or a uniprot id")
                

    def __str__(self):
        return f"{self.sequence}"