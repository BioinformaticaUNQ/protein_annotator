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
    
def donwload_uniprot_db(path_to_download)-> object:
    with tempfile.NamedTemporaryFile() as download_file:
#        url = "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz"
        url = "https://getsamplefiles.com/download/zip/sample-5.zip"
        with httpx.stream("GET", url, timeout=None) as response:
            total = int(response.headers["Content-Length"])            
            with tqdm(total=total, unit_scale=True, unit_divisor=1024, unit="B") as progress:
                num_bytes_downloaded = response.num_bytes_downloaded
                for chunk in response.iter_bytes():
                    download_file.write(chunk)
                    #print(download_file)
                    progress.update(response.num_bytes_downloaded - num_bytes_downloaded)
                    num_bytes_downloaded = response.num_bytes_downloaded
        file_name = download_file.name
        ptint('file_name: '+ file_name)
        shutil.copy(file_name, path_to_download+'sample-5.zip')                    
        return download_file

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
