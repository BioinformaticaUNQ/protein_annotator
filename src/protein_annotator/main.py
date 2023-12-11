from protein_annotator.annotate_dbs.uniprot_querys_db import * 
from protein_annotator.annotate_dbs.uniprot_querys_api import *
import json
from protein_annotator.annotate_dbs.parse_prote_txt import *
from protein_annotator.annotate_dbs.biolip_query_annotate import *

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

def annotate_site(uniprot_id, residue_number, path_db_uniprot, path_biolip)-> object:
    '''
    uniprot_id: id de la proteina  en la base de datos uniprot
    residue_number: posicion en secuencia
    path_db: directorio donde se encuentra la base de datos local
    '''
    #TODO: try catchc
    #obtengo la proteina de la bd uniprot
    annot_uniprot = annotate_site_uniprot(uniprot_id, residue_number,path_db_uniprot)
    annot_biolip = annotate_site_biolip(path_biolip,uniprot_id, residue_number)
    
    return { uniprot_id : [ annot_uniprot , annot_biolip]}
    
def annotate_protein(uniprot_id, path_db_uniprot, path_biolip):
    res_biolip = annotate_biolip(path=path_biolip, uniprot_id=uniprot_id)
    res_uniprot = annotate_uniprot(path_db=path_db_uniprot,uniprot_id=uniprot_id)
    
    ret = { uniprot_id: { "biolip": res_biolip, "uniprot": res_uniprot } }
    return ret