from protein_annotator.uniprot.uniprot_querys_db import * 
from protein_annotator.uniprot.uniprot_querys_api import *
import json
from protein_annotator.uniprot.parse_prote_txt import *

def say_hi() -> str:
    return "hi!"

def get_protein_by_db(uniprot_id, path_db) -> str:
    return get_protein_db(uniprot_id, path_db)


''' obtiene una prote de uniprot via API'''
def get_protein_by_api(uniprot_id) -> object:
    return get_protein_api(uniprot_id)


def download_file(path,url_dwn, file_name):
    ''' 
    path: directorio donde se va a descargar el archivo. 
    url_dwn: url de descarga, tiene que ser HTTP GET 
    file_name: nombre del archivo que con el que se va a almacenar,
    '''
    download_f(path, url_dwn, file_name)

def download_uniport_db(path):
    download_f(path, "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz", "uniprot_sprot.dat.gz")

def parse_biolib(path):
    parse_biolib_db(path)

    
def download_biolip_db(path):
    download_f(path,"https://zhanggroup.org/BioLiP/download/BioLiP.txt.gz", "BioLiP.txt.gz")



def annotate_site(uniprot_id, residue_number, path_db)-> object:
    '''
    uniprot_id: id de la proteina  en la base de datos uniprot
    residue_number: posicion en secuencia
    path_db: directorio donde se encuentra la base de datos local
    '''
    #obtengo la proteina de la bd uniprot
    prot = get_protein_by_db(uniprot_id, path_db)
    #filtro de la listo de  objetos features los que son bindings.
    lis_b = filter(lambda p: p.type=='BINDING', prot.features)
    ligando = ''
    res = None
    #recorro los bindings para revisar si alguno correspoonde con la posicion que viene por parametro.     
    for bind in lis_b:
        #valido si estra entre el inicio y el final de la posicion.
        if(bind.location.start <= residue_number) and (bind.location.end >= residue_number):
            print(bind.qualifiers['ligand'])
            #si en la posicion existe melo guardo. 
            ligando = bind.qualifiers['ligand']
            print('lo encontre')
            #armo un objeto  json para poder retornar el resultado
            res = json.loads('{ "uniprot_id":"'+str(uniprot_id)+'", "uniport": {"residue_number": "'+str(residue_number)+'", "ligand":"'+str(ligando)+'"} }')
            break            
        else:
            return json.loads('{ "msg":" no se encontro el ligando en la posicion "}')
    return res
    