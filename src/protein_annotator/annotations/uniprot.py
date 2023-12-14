from typing import Any, Dict, List

from Bio.SeqRecord import SeqRecord


def annotate_site_uniprot(protein: SeqRecord, residue_number: int) -> Dict[str, Any]:
    """Annotates site using Uniprot

    Args:
        protein (SeqRecord): sequence information
        residue_number (int): position in sequence

    Returns:
        Dict[str, Any]: annotated site
    """
    annotation: Dict[str, Any] = {}

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


def annotate_uniprot(protein: SeqRecord) -> List[Dict[str, Any]]:
    """Annotates the protein associated to the Uniprot ID

    Args:
        protein: (SeqRecord): sequence information

    Returns:
        List[Dict[str, Any]]: annotated protein
    """

    annotations: List[Dict[str, Any]] = []

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
