from protein_annotator.uniprot.uniprot_querys_db import * 
from protein_annotator.uniprot.uniprot_querys_api import *
 
def say_hi() -> str:
    return "hi!"

def get_protein_by_db(uniprot_id, path_db) -> str:
    return get_protein_db(uniprot_id, path_db)


def get_protein_by_api(uniprot_id) -> object:
    return get_protein_api(uniprot_id)

def donwnload_uniprot(path_src):
    donwload_uniprot_db(path_src)

