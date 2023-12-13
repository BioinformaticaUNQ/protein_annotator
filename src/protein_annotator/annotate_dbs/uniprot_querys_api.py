from io import StringIO

import httpx
from Bio import SwissProt
from Bio.SwissProt import Record


def get_protein_api(uniprod_id: str) -> Record:
    response = httpx.get(f"https://rest.uniprot.org/uniprotkb/{uniprod_id}?format=txt")
    record = SwissProt.read(StringIO(response.text))
    return record
