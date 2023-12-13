from typing import Any, Dict, List

from protein_annotator.annotations.dbs import get_protein_from_db


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

    protein = get_protein_from_db(uniprot_id, db_path)
    if not protein:
        return None

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

    protein = get_protein_from_db(uniprot_id, db_path)
    if not protein:
        return None

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
