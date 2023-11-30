from pathlib import Path
from Bio import SeqIO
import httpx
import json
from protein_annotator.schemas import ProteinData

def file_exists(path) -> bool:
  """
  Indica si un archivo existe

  Args:
    path: ruta del archivo

  Returns:
    True si el archivo existe, False sino
  """
  file = Path(path)
  return file.exists()

def is_fasta(path) -> bool:
  """
  Indica si un archivo es del tipo FASTA validando existencia y extension

  Args:
    path: ruta del archivo

  Returns:
    True si el archivo cumple la condicion, False sino la cumple
  """
  status = file_exists(path) and Path(path).suffix=='.fasta'
  return status
  

# def load_uniprot_db(db_path):
#   """
#   Carga la base de datos UniProt en una ubicación local.

#   Args:
#     db_path: La ruta al archivo `.dat.gz` que contiene la base de datos UniProt.

#   Returns:
#     Un iterable sobre la base de datos UniProt cargada.
#   """
#   # return UniProtKB.LocalData.load(db_path)
#   handle = gzip.open(db_path)
#   return SwissProt.parse(handle)


def is_uniprot_id(input:str):
  """
  Decide si un input dado corresponde a un uniprot id

  Args:
    input: El input a evaluar.

  Returns:
    True si el input corresponde a un uniprot id, False en caso contrario.
  """
  try:
    get_fasta_from_uniprot(input)
    return True
  except httpx.RequestError as exc:
    return False
  

def parse_fasta(path) -> ProteinData:
  """
  Parsea un archivo FASTA y desensambla sus componentes

  Args:
    path: ruta del archivo

  Returns:
    un dict con los atributos id, descripcion y secuencia
  """
  results = []
  for seq_record in SeqIO.parse(path, "fasta"):
    id, description = get_data_from_description(seq_record.id)
    results.append(ProteinData(id,description, get_sequence_from_seq(seq_record.seq._data.decode()), seq_record))
  return results[0]
  
  """
  Obtiene un dict con la secuencia y descripcion a partir de un uniprotID

  Args:
    uniprot_id: identificador uniprot

  Returns:
    un dict con los atributos id, descripcion y secuencia
  """
def get_fasta_from_uniprot(uniprot_id) -> ProteinData:
  query = str(uniprot_id)+".json"
  try:
    result = httpx.get('https://www.uniprot.org/uniprotkb/'+query, follow_redirects=True)
    result.raise_for_status()
    parsedResponse = json.loads(result.text)
    print(parsedResponse)
    return ProteinData(parsedResponse['uniProtkbId'],'',parsedResponse['sequence']['value'], parsedResponse)
  except Exception as e:
    raise e



def get_sequence_from_seq(seq) -> str:
  return seq.replace('\')','').removeprefix('Seq(\'')

def get_data_from_description(desc: str) -> tuple[str,str]:
  splitted = desc.split('.')
  return (splitted[0], '') if len(splitted)<2 else (splitted[0], splitted[1])
