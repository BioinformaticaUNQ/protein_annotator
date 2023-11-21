from Bio import SeqIO
from protein_annotator.uniprot import parse_prote_txt as parser
from io import StringIO
import codecs 
import httpx
import tempfile
from tqdm import tqdm


def get_protein_db(uniprod_id, path_db)-> object:    
    
    uniprot = SeqIO.index(path_db, "swiss")
    prot = uniprot.get_raw(uniprod_id)
    record = parser.parse(StringIO(codecs.decode(prot, 'utf-8')))
    
    return record
    
def donwload_uniprot_db(path_to_download)-> object:

    with tempfile.NamedTemporaryFile() as download_file:
 #       url = "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz"
        url = "https://getsamplefiles.com/download/gzip/sample-5.gz"
        with httpx.stream("GET", url, timeout=None) as response:
            total = int(response.headers["Content-Length"])
            
            with tqdm(total=total, unit_scale=True, unit_divisor=1024, unit="B") as progress:
                num_bytes_downloaded = response.num_bytes_downloaded
                for chunk in response.iter_bytes():
                    download_file.write(chunk)
                    progress.update(response.num_bytes_downloaded - num_bytes_downloaded)
                    num_bytes_downloaded = response.num_bytes_downloaded
                    print(response)
            with open(path_to_download+'file_name.pdf', 'wb') as f:
                f.write(download_file.NamedTemporaryFile())
            return download_file