from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest
from Bio.Blast import NCBIXML
from Bio.Blast.Record import Blast

from protein_annotator.homologs import get_homologs


@pytest.fixture
def blast_result() -> Blast:
    filename_path = Path(__file__).parent / "data" / "blast.xml"
    with open(filename_path) as f:
        data = NCBIXML.read(f)
    return data


def test_get_homologs(blast_result: StringIO) -> None:
    # Arrange
    fasta_file = Path(__file__).parent / "data" / "query.fasta"

    assert fasta_file.exists()

    # Act
    with patch("protein_annotator.homologs._run_blast") as run_blast_mock:
        run_blast_mock.return_value = blast_result
        hits = get_homologs(query=str(fasta_file.resolve()), db="../testdb")

    # Assert
    assert len(hits) == 2
    assert hits[0]["uniprot_id"] == "P99998"
    assert hits[0]["coverage"] == 100.0
    assert hits[0]["description"] == (
        "RecName: Full=Cytochrome c [Pan troglodytes] >sp|P99999.2| RecName: "
        "Full=Cytochrome c [Homo sapiens] >sp|Q5RFH4.3| RecName: Full=Cytochrome "
        "c [Pongo abelii] >sp|Q6WUX8.3| RecName: Full=Cytochrome c [Gorilla gorilla gorilla]"
    )
    assert hits[0]["e_value"] == 1.31049e-73
    assert hits[0]["id_percentage"] == 100.0
    assert hits[0]["sequence"] == (
        "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIW"
        "GEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE"
    )
