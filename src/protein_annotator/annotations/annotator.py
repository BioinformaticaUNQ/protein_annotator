from typing import Any, Dict

from protein_annotator.annotations.biolip import annotate_biolip, annotate_site_biolip
from protein_annotator.annotations.uniprot import (
    annotate_site_uniprot,
    annotate_uniprot,
)


def annotate_site(
    uniprot_id: str,
    residue_number: int,
    path_db_uniprot: str,
    path_biolip: str,
) -> Dict[str, Any]:
    uniprot_annotation = annotate_site_uniprot(
        uniprot_id,
        residue_number,
        path_db_uniprot,
    )
    #Cortamos aca porque si no esta en uniprot por uniprot id directamente no existe en biolip
    if(uniprot_annotation is None):
        return { "uniprot_id": "uniprot_id invalido o inexistente en la base de datos" }

    biolip_annotation = annotate_site_biolip(
        path_biolip,
        uniprot_id,
        residue_number,
    )
    return {
        "uniprot_id": uniprot_id,
        "biolip_annotation": biolip_annotation,
        "uniprot_annotation": uniprot_annotation,
    }


def annotate_protein(
    uniprot_id: str, path_db_uniprot: str, path_biolip: str
) -> Dict[str, Any]:
    uniprot_annotations = annotate_uniprot(
        db_path=path_db_uniprot,
        uniprot_id=uniprot_id,
    )
    #Cortamos aca porque si no esta en uniprot por uniprot id directamente no existe en biolip
    if(uniprot_annotations is None):
        return { "uniprot_id": "uniprot_id invalido o inexistente en la base de datos" }
    
    biolip_annotations = annotate_biolip(
        path=path_biolip,
        uniprot_id=uniprot_id,
    )
    return {
        "uniprot_id": uniprot_id,
        "biolip_annotations": biolip_annotations,
        "uniprot_annotations": uniprot_annotations,
    }
