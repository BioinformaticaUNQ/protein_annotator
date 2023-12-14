from typing import Any, Dict

from protein_annotator.annotations.biolip import annotate_biolip, annotate_site_biolip
from protein_annotator.annotations.dbs import get_record_from_uniprot_db
from protein_annotator.annotations.uniprot import (
    annotate_site_uniprot,
    annotate_uniprot,
)


def annotate_site(
    uniprot_id: str,
    residue_number: int,
    uniprot_db_path: str,
    biolip_db_path: str,
) -> Dict[str, Any]:
    protein = get_record_from_uniprot_db(uniprot_id, uniprot_db_path)

    uniprot_annotation = annotate_site_uniprot(protein, residue_number)
    biolip_annotation = annotate_site_biolip(protein.id, residue_number, biolip_db_path)

    return {
        "uniprot_id": uniprot_id,
        "biolip_annotation": biolip_annotation,
        "uniprot_annotation": uniprot_annotation,
    }


def annotate_protein(
    uniprot_id: str, uniprot_db_path: str, biolip_db_path: str
) -> Dict[str, Any]:
    protein = get_record_from_uniprot_db(uniprot_id, uniprot_db_path)

    uniprot_annotations = annotate_uniprot(protein)
    biolip_annotations = annotate_biolip(protein.id, biolip_db_path)

    return {
        "uniprot_id": protein.id,
        "biolip_annotations": biolip_annotations,
        "uniprot_annotations": uniprot_annotations,
    }
