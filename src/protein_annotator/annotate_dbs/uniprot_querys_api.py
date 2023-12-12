import httpx
from protein_annotator.annotate_dbs import parse_prote_txt as parser
from io import StringIO

def get_protein_api(uniprod_id) -> object:

    prot = httpx.get('https://rest.uniprot.org/uniprotkb/'+str(uniprod_id)+'?format=txt')
    record = parser.parse(StringIO(prot.text))    

    return record