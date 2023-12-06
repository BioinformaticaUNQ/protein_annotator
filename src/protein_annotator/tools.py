from pathlib import Path

import httpx
from Bio import SeqIO

from protein_annotator.schemas import ProteinData


def is_fasta(path: str) -> bool:
    """Indica si un archivo es del tipo FASTA validando existencia y extension

    Args:
      path: ruta del archivo

    Returns:
      True si el archivo cumple la condicion, False sino la cumple
    """
    file_path = Path(path)
    return file_path.exists() and file_path.suffix == ".fasta"


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


def is_uniprot_id(uniprot_id: str):
    """Decide si un id dado corresponde a un uniprot id

    Args:
      uniprot_id: El id a evaluar.

    Returns:
      True si el uniprot_id corresponde a un uniprot id, False en caso contrario.
    """
    try:
        get_fasta_from_uniprot(uniprot_id)
        return True
    except Exception:
        return False


def parse_fasta(path: str) -> ProteinData:
    """Parsea un archivo FASTA y desensambla sus componentes

    Args:
      path: ruta del archivo

    Returns:
      un dict con los atributos id, descripcion y secuencia
    """
    results = []
    for seq_record in SeqIO.parse(path, "fasta"):
        protein_id, protein_description = get_data_from_description(seq_record.id)
        results.append(
            ProteinData(
                protein_id,
                protein_description,
                get_sequence_from_seq(seq_record.seq._data.decode()),
                seq_record,
            )
        )
    return results[0]


def get_fasta_from_uniprot(uniprot_id: str) -> ProteinData:
    """
    Obtiene un dict con la secuencia y descripcion a partir de un uniprotID

    Args:
      uniprot_id: identificador uniprot

    Returns:
      un ProteinData con los atributos id, descripcion y secuencia
    """
    try:
        result = httpx.get(
            f"https://www.uniprot.org/uniprotkb/{uniprot_id}.json",
            follow_redirects=True,
        )
        result.raise_for_status()

        parsed_response = result.json()

        return ProteinData(
            parsed_response["uniProtkbId"],
            "",
            parsed_response["sequence"]["value"],
            parsed_response,
        )

    except Exception as e:
        raise e


def get_sequence_from_seq(seq) -> str:
    return seq.replace("')", "").removeprefix("Seq('")


def get_data_from_description(desc: str) -> tuple[str, str]:
    splitted = desc.split(".")
    return (splitted[0], "") if len(splitted) < 2 else (splitted[0], splitted[1])
