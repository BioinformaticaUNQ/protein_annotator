from Bio import SeqIO
from Bio.bgzf import *
from protein_annotator.annotate_dbs import parse_prote_txt as parser
from io import StringIO
import codecs 
import httpx
import tempfile
from tqdm import tqdm
import shutil, os
import gzip
from protein_annotator.annotate_dbs.uniprot_querys_api import *
import json
from protein_annotator.annotate_dbs.parse_prote_txt import *

def get_protein_db(uniprod_id, path_db)-> object:    
    
    with gzip.open(path_db, 'rb') as handle:
       #niprot = SeqIO.index(handle, "swiss") 
       try:
        uniprot = SeqIO.parse(handle,  "swiss")        
#       uni = filter(lambda seq : seq.id == str(uniprod_id), uniprot)
        for pr in uniprot:
            if(pr.id == uniprod_id):
                uni = pr   
                record = pr
                break
       except:
            return None
       return record
    
'''
def get_protein_db(uniprod_id, path_db)-> object:    
    
    
    ddbb = gzip.open(path_db,'rb')
    ddbb_file = ddbb.read()
    uniprot = SeqIO.index(ddbb_file, "swiss")
    prot = uniprot.get_raw(uniprod_id)
    record = parser.parse(StringIO(codecs.decode(prot, 'utf-8')))
    
    return record
'''    

def download_f(path_to_download, url_dwn, file_name) -> object:

    # TODO: agregar try catch exception

    with tempfile.NamedTemporaryFile(delete=False) as download_file:
        url = url_dwn
        with httpx.stream("GET", url, timeout=None) as response:
            total = int(response.headers["Content-Length"])            
            with tqdm(total=total, unit_scale=True, unit_divisor=1024, unit="B") as progress:
                num_bytes_downloaded = response.num_bytes_downloaded
                for chunk in response.iter_bytes():
                    download_file.write(chunk)
                    progress.update(response.num_bytes_downloaded - num_bytes_downloaded)
                    num_bytes_downloaded = response.num_bytes_downloaded
        file_ = download_file.name
        shutil.copy(file_, path_to_download+file_name)                    
        return download_file

def annotate_site_uniprot(uniprot_id, residue_number, path_db)-> object:
    '''
    uniprot_id: id de la proteina  en la base de datos uniprot
    residue_number: posicion en secuencia
    path_db: directorio donde se encuentra la base de datos local
    '''
    #TODO: try catchc
    #obtengo la proteina de la bd uniprot
    prot = get_protein_db(uniprot_id, path_db)
    if(prot is None):
        return json.loads('{ "uniprot":" no se encuentra la proteina para ese id "}') 
    #filtro de la listo de  objetos features los que son bindings.
    lis_b = list(filter(lambda p: p.type=='BINDING' or p.type == 'ACT_SITE', prot.features))
    
    ligando = ''
    res = None
    #recorro los bindings para revisar si alguno correspoonde con la posicion que viene por parametro.     
    for bind in lis_b:
        #valido si estra entre el inicio y el final de la posicion.
        if(int(bind.location.start) <= residue_number) and (residue_number <= int(bind.location.end)):
            if bind.type == 'BINDING':
                #si en la posicion existe melo guardo. 
                ligando = bind.qualifiers['ligand']
                #armo un objeto  json para poder retornar el resultado # agregar residuo a que se corresponde. ej: lisina 100. 
                res = json.loads('{  "uniprot": {"residue_number": "'+str(residue_number)+'", "residue": "'+str(prot.seq[residue_number-1])+'" , "ligand":"'+str(ligando)+'"} }')
            else:
                res = json.loads('{  "uniprot": {"residue_number": "'+str(residue_number)+'", "residue": "'+str(prot.seq[residue_number-1])+'" , "ligand":"'+str(None)+'"} }')                
                
    if res == None:
        res =  json.loads('{ "uniprot":" no se encontro el ligando en la posicion "}')        
    return res
    
def annotate_uniprot(uniprot_id, path_db)-> object:
    '''
    uniprot_id: id de la proteina  en la base de datos uniprot
    residue_number: posicion en secuencia
    path_db: directorio donde se encuentra la base de datos local
    '''
    #TODO: try catchc
    #obtengo la proteina de la bd uniprot
    prot = get_protein_db(uniprot_id, path_db)
    if(prot is None):
        return json.loads('{ "uniprot":" no se encuentra la proteina para ese id "}') 
    #filtro de la listo de  objetos features los que son bindings.
    lis_b = list(filter(lambda p: p.type=='BINDING' or p.type == 'ACT_SITE', prot.features))
    
    ligando = ''
    #recorro los bindings para revisar si alguno correspoonde con la posicion que viene por parametro.     
    lis = []
    for bind in lis_b:
        print('bind' + str(bind))
        #valido si estra entre el inicio y el final de la posicion.
        if bind.type == 'BINDING':
            #si en la posicion existe melo guardo. 
            ligando = bind.qualifiers['ligand']
            #armo un objeto  json para poder retornar el resultado # agregar residuo a que se corresponde. ej: lisina 100. 
            #res = json.loads('{  "uniprot": {"residue_number": "'+str(residue_number)+'", "residue": "'+str(prot.seq[residue_number-1])+'" , "ligand":"'+str(ligando)+'"} }')
            lis.append(json.loads('{"residue_location": "'+str(bind.location)+'" , "ligand":"'+str(ligando)+'"} '))
        else:
                #res = json.loads('{  "uniprot": {"residue_number": "'+str(residue_number)+'", "residue": "'+str(prot.seq[residue_number-1])+'" , "ligand":"'+str(None)+'"} }')                
            lis.append(json.loads('{"residue_location": "'+str(bind.location)+'" , "ligand":"'+str(None)+'"}'))    
    return lis
