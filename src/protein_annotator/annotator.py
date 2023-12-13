from typing import Any, Dict, List

from protein_annotator.annotate_dbs.biolip_query_annotate import (
    annotate_biolip,
    annotate_site_biolip,
)
from protein_annotator.annotate_dbs.uniprot_querys_db import (
    annotate_site_uniprot,
    annotate_uniprot,
    download_file,
)


def download_uniport_db(path: str) -> None:
    download_file(
        path,
        "https://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/complete/uniprot_sprot.dat.gz",
        "uniprot_sprot.dat.gz",
    )


def download_biolip_db(path: str) -> None:
    download_file(
        path,
        "https://zhanggroup.org/BioLiP/download/BioLiP.txt.gz",
        "BioLiP.txt.gz",
    )


def annotate_site(
    uniprot_id: str,
    residue_number: int,
    path_db_uniprot: str,
    path_biolip: str,
) -> Dict[str, List[Dict[str, Any]]]:
    biolip_annotation = annotate_site_biolip(
        path_biolip,
        uniprot_id,
        residue_number,
    )
    uniprot_annotation = annotate_site_uniprot(
        uniprot_id,
        residue_number,
        path_db_uniprot,
    )
    return {
        "uniprot_id": uniprot_id,
        "biolip_annotation": biolip_annotation,
        "uniprot_annotation": uniprot_annotation,
    }


def annotate_protein(
    uniprot_id: str, path_db_uniprot: str, path_biolip: str
) -> Dict[str, Dict[str, Any]]:
    biolip_annotations = annotate_biolip(
        path=path_biolip,
        uniprot_id=uniprot_id,
    )
    uniprot_annotations = annotate_uniprot(
        db_path=path_db_uniprot,
        uniprot_id=uniprot_id,
    )
    return {
        "uniprot_id": uniprot_id,
        "biolip_annotations": biolip_annotations,
        "uniprot_annotations": uniprot_annotations,
    }
