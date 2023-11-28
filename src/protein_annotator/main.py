from protein_annotator.uniprot.uniprot_querys_db import * 
from protein_annotator.uniprot.uniprot_querys_api import *
import json
 
def say_hi() -> str:
    return "hi!"

def get_protein_by_db(uniprot_id, path_db) -> str:
    return get_protein_db(uniprot_id, path_db)


def get_protein_by_api(uniprot_id) -> object:
    return get_protein_api(uniprot_id)

def download_file(path,url_dwn, file_name):
    download_f(path, url_dwn, file_name)

def annotate_site(uniprot_id, residue_number, path_db)-> object:

    prot = get_protein_by_db(uniprot_id, path_db)
    lis_b = filter(lambda p: p.type=='BINDING', prot.features)
    ligando = ''
    res = None
    for bind in lis_b:
        if(bind.location.start <= residue_number) and (bind.location.end >= residue_number):
            print(bind.qualifiers['ligand'])
            ligando = bind.qualifiers['ligand']
            print('lo encontre')
            res = json.loads('{ "uniprot_id":"'+str(uniprot_id)+'", "residue_number": "'+str(residue_number)+'", "ligand":"'+str(ligando)+'"}')
            break            
        else:
            return json.loads('{ "msg":" no se encontro el ligando en la posicion "}')
    return res
    