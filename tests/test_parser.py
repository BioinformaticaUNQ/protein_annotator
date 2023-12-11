from pathlib import Path

from protein_annotator.parser import InputParser


def test_create_new_instance_with_fasta_file_path() -> None:
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
    assert sequence.accession == fasta_id
    assert sequence.description == fasta_desc
    assert sequence.sequence == fasta_seq

    filename_path.unlink()


def test_create_new_instance_with_uniprot_id() -> None:
    # Arrange
    uniprot_id = "Q8I6R7"

    # Act / SUT
    sequence = InputParser.parse(uniprot_id)

    # Assert
    assert sequence.accession == "ACN2_ACAGO"
    assert sequence.sequence == (
        "DVYKGGGGGRYGGGRYGGGGGYGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGG"
        "GLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGRGGYGGGGYGGGY"
        "GGGYGGGKYKG"
    )
