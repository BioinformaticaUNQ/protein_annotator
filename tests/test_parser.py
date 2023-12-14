from pathlib import Path
from unittest.mock import Mock, patch

import httpx
import pytest

# from protein_annotator.annotations.dbs import download_uniprot_db
from protein_annotator.parser import InputParser


@pytest.fixture
def uniprot_response() -> str:
    filename_path = Path(__file__).parent / "data" / "uniprot.xml"
    with open(filename_path) as f:
        data = f.read()
    return data


def test_parse_fasta_file() -> None:
    # Arrange
    fasta_id = "NP_061820"
    fasta_desc = "1_cytochrome_c_[Homo_sapiens]"
    fasta_seq = (
        "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIW"
        "GEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE"
    )

    fasta_file_content = f">{fasta_id}.{fasta_desc}\n{fasta_seq}"

    filename_path = Path(__file__).parent / "test.fasta"
    filename_path.touch(exist_ok=True)

    with open(filename_path, "w+") as f:
        f.write(fasta_file_content)

    # Act / SUT
    sequence = InputParser.parse(str(filename_path.resolve()))

    # Asert
    assert sequence.uniprot_id == fasta_id
    assert sequence.description == f"{fasta_id}.{fasta_desc}"
    assert sequence.sequence == fasta_seq

    filename_path.unlink()


def test_parse_fasta_file_with_header_in_another_format() -> None:
    # Arrange
    fasta_id = "P99998"
    fasta_desc = "CYC_PANTR Cytochrome c OS=Pan troglodytes OX=9598 GN=CYCS PE=1 SV=2"
    fasta_seq = (
        "MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIW"
        "GEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE"
    )

    fasta_file_content = f">sp|{fasta_id}|{fasta_desc}\n{fasta_seq}"

    filename_path = Path(__file__).parent / "test.fasta"
    filename_path.touch(exist_ok=True)

    with open(filename_path, "w+") as f:
        f.write(fasta_file_content)

    # Act / SUT
    sequence = InputParser.parse(str(filename_path.resolve()))

    # Asert
    assert sequence.uniprot_id == fasta_id
    assert sequence.description == f"sp|{fasta_id}|{fasta_desc}"
    assert sequence.sequence == fasta_seq

    filename_path.unlink()


def test_parse_uniprot_id(uniprot_response: Mock) -> None:
    # Arrange
    uniprot_id = "Q8I6R7"

    # Act / SUT
    with patch("protein_annotator.annotations.dbs.httpx.get") as httpx_get_mock:
        httpx_get_mock.return_value = httpx.Response(
            200,
            text=uniprot_response,
            request=httpx.Request(
                "GET",
                f"https://www.uniprot.org/uniprotkb/{uniprot_id}.xml",
            ),
        )
        sequence = InputParser.parse(uniprot_id)

    # Assert
    assert sequence.uniprot_id == "Q8I6R7"
    assert sequence.sequence == (
        "DVYKGGGGGRYGGGRYGGGGGYGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGG"
        "GLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGRGGYGGGGYGGGY"
        "GGGYGGGKYKG"
    )


# def test_parse_uniprot_id_with_local_db(uniprot_response: Mock) -> None:
#     # Arrange
#     db_path = Path(__file__).parent / "data" / "uniprot_sprot.dat.gz"
#     uniprot_id = "Q8I6R7"
#     if not Path(db_path).is_file():
#         download_uniprot_db(db_path.parent)

#     # Act / SUT
#     sequence = InputParser.parse(uniprot_id, db_path)

#     # Assert
#     assert sequence.uniprot_id == "Q8I6R7"
#     assert sequence.sequence == (
#         "DVYKGGGGGRYGGGRYGGGGGYGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGG"
#         "GLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGRGGYGGGGYGGGY"
#         "GGGYGGGKYKG"
#     )
