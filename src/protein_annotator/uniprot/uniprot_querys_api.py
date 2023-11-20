import httpx

def get_protein_api(uniprod_id) -> object:
    prot = httpx.get('https://rest.uniprot.org/uniprotkb/'+str(uniprod_id)+'?format=txt')
    return prot