import gzip
import logging
import pathlib
from typing import Any, Dict, List

import httpx
from Bio import SeqIO
from Bio.SeqIO.SwissIO import SwissIterator
from Bio.SeqRecord import SeqRecord
from tqdm import tqdm

logger = logging.getLogger()


def get_protein_db(uniprod_id: str, path_db: str) -> SeqRecord:
    found_record = None
    with gzip.open(path_db, "rb") as handle:
        try:
            records: SwissIterator = SeqIO.parse(handle, "swiss")
            found_record = next(
                (record for record in records if record.id == uniprod_id), None
            )
            return found_record
        except Exception:
            return found_record


def download_file(path_to_download: str, url: str, file_name: str) -> pathlib.Path:
    file_path = pathlib.Path(path_to_download) / file_name
    if file_path.exists():
        raise ValueError("File already exists")
    if file_path.is_dir():
        raise ValueError("File name must not be a directory")

    try:
        with open(file_path, "wb") as file_out:
            with httpx.stream(
                method="GET", url=url, follow_redirects=True, timeout=60
            ) as response:
                response.raise_for_status()

                file_size = int(response.headers.get("Content-Length", 0))
                desc = f"Downloading: {url}"

                for chunk in tqdm(
                    iterable=response.iter_raw(1),
                    desc=desc,
                    unit="B",
                    unit_scale=True,
                    unit_divisor=1024,
                    total=file_size,
                ):
                    file_out.write(chunk)

        return file_path
    except Exception as e:
        logger.exception(f"Error while downloading file {url}")
        file_path.unlink()
        raise e


def annotate_site_uniprot(
    uniprot_id: str, residue_number: int, db_path: str
) -> Dict[str, Any]:
    """Annotates site using Uniprot

    Args:
        uniprot_id (str): Uniprot protein id
        residue_number (int): position in sequence
        db_path (str): path to the database file

    Returns:
        Dict[str, Any]: annotated site
    """
    annotation: Dict[str, Any] = {}

    protein = get_protein_db(uniprot_id, db_path)
    if not protein:
        return annotation

    # filters protein features by type
    bindings = (
        feature
        for feature in protein.features
        if feature.type in ("BINDING", "ACT_SITE")
    )

    # traverses through the bindings list and check if any matches the residue_number
    for bind in bindings:
        if int(bind.location.start) <= residue_number <= int(bind.location.end):
            ligand = bind.qualifiers["ligand"] if bind.type == "BINDING" else None
            # adds the associated residue, i.e.: lisine 100
            annotation = {
                "residue_number": residue_number,
                "residue": protein.seq[residue_number - 1],
                "ligand": ligand,
            }
            break
    return annotation


def annotate_uniprot(uniprot_id: str, db_path: str) -> List[Dict[str, Any]]:
    """Annotates the protein associated to the Uniprot ID

    Args:
        uniprot_id (str): Uniprot protein id
        db_path (str): path to the database file

    Returns:
        List[Dict[str, Any]]: _description_
    """

    annotations: List[Dict[str, Any]] = []

    protein = get_protein_db(uniprot_id, db_path)
    if not protein:
        return annotations

    # filters protein features by type
    bindings = (
        feature
        for feature in protein.features
        if feature.type in ("BINDING", "ACT_SITE")
    )

    for bind in bindings:
        ligand = bind.qualifiers["ligand"] if bind.type == "BINDING" else None
        annotations.append(
            {
                "residue_number": str(bind.location),
                "ligand": ligand,
            }
        )
    return annotations
