from protein_annotator.uniprot.uniprot_querys_db import * 
 
def say_hi() -> str:
    return "hi!"

def get_protein(uniprot_id) -> str:
    return get_protein_db(uniprot_id, "/home/mauro/Descargas/uniprot_sprot.dat","uniprot_sprot.dat")