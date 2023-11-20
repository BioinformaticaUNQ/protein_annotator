from protein_annotator.uniprot.uniprot_querys_db import * 
from protein_annotator.uniprot.uniprot_querys_api import *
 
def say_hi() -> str:
    return "hi!"

def get_protein_by_db(uniprot_id) -> str:
    return get_protein_db(uniprot_id, "/home/mauro/Descargas/uniprot_sprot.dat","uniprot_sprot.dat")


def get_protein_by_api(uniprot_id) -> object:
    return get_protein_api(uniprot_id)
