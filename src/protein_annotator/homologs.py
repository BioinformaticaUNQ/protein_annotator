from io import StringIO
from pathlib import Path
from typing import Any, Dict, List, Optional

from Bio.Blast import NCBIWWW, NCBIXML
from Bio.Blast.Applications import NcbiblastpCommandline
from Bio.Blast.Record import Blast

from protein_annotator import logger
from protein_annotator.parser import InputParser, get_uniprot_id_from_accession


def _run_blast(
    query: str,
    db: str,
    threshold: int,
    max_hits: int,
    uniprot_db: Optional[str] = None,
) -> Blast:
    if Path(query).exists() and Path(db).exists():
        logger.info(
            f"Local execution of blastp for {query=} {db=} {threshold=} {max_hits=}"
        )
        blastp_command = NcbiblastpCommandline(
            db=db,
            query=query,
            outfmt=5,  # Blast XML
        )
        stdout, _ = blastp_command()  # noqa
        query_result = StringIO(stdout)

    else:
        protein = InputParser.parse(query, uniprot_db)
        logger.info(
            f"Remote execution of blastp for {query=} {db=} {threshold=} {max_hits=}"
        )
        query_result = NCBIWWW.qblast(
            "blastp",
            db,
            protein.sequence,
            format_type="XML",
        )

    try:
        blast: Blast = NCBIXML.read(query_result)
    except Exception as e:
        raise ValueError("Can not parse the blastp result") from e
    finally:
        query_result.close()

    return blast


def get_homologs(
    *,
    query: str,
    db: str,
    threshold: int = 40,
    max_hits: int = 10,
    uniprot_db: Optional[str] = None,
) -> List[Dict[str, Any]]:
    blast = _run_blast(query, db, threshold, max_hits, uniprot_db)

    hits = []
    for alignment in blast.alignments:
        for hsp in alignment.hsps:
            id_percentage = round(hsp.identities / hsp.align_length, 2) * 100
            if id_percentage >= threshold:
                hits.append(
                    dict(
                        uniprot_id=get_uniprot_id_from_accession(alignment.hit_id),
                        description=alignment.hit_def,
                        sequence=hsp.sbjct,
                        coverage=len(hsp.sbjct) / len(hsp.query) * 100,
                        e_value=hsp.expect,
                        id_percentage=id_percentage,
                    )
                )
    return hits[:max_hits]
