from Bio import SeqIO
from protein_annotator.uniprot import parse_prote_txt as parser
from io import StringIO
import codecs 
import httpx
import tempfile
from tqdm import tqdm
import shutil, os
import gzip

def get_protein_db(uniprod_id, path_db)-> object:    
    
    
    uniprot = SeqIO.index(path_db, "swiss")
    prot = uniprot.get_raw(uniprod_id)
    record = parser.parse(StringIO(codecs.decode(prot, 'utf-8')))
    
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
