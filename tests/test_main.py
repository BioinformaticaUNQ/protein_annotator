from pathlib import Path
from protein_annotator.main import ProteinAnnotator

def test_instance_fasta_protein() -> None:
    
     # SUT
    fastaSequence = '''>NP_061820.1_cytochrome_c_[Homo_sapiens]
MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE'''
    # Expected
    fasta_id = 'NP_061820'
    fasta_desc = '1_cytochrome_c_[Homo_sapiens]'
    fasta_seq = 'MGDVEKGKKIFIMKCSQCHTVEKGGKHKTGPNLHGLFGRKTGQAPGYSYTAANKNKGIIWGEDTLMEYLENPKKYIPGTKMIFVGIKKKEERADLIAYLKKATNE'

    current_dir = Path(__file__).parent
    filename = "test.fasta"
    file_to_open = current_dir/Path(filename)

    file_to_open.touch(exist_ok= True)
    with open(file_to_open,"w+") as f:
        f.write(fastaSequence)


    protein = ProteinAnnotator(filename)
    assert protein.protein_data.id==fasta_id
    assert protein.protein_data.description==fasta_desc
    assert protein.protein_data.sequence==fasta_seq



def test_new_uniprot_protein() -> None:
    
    uniprot_sequence = 'Q8I6R7'

    protein = ProteinAnnotator(uniprot_sequence)
    assert protein.protein_data.id=='ACN2_ACAGO'
    assert protein.protein_data.sequence=='DVYKGGGGGRYGGGRYGGGGGYGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGGLGGGGLGGGKGLGGGGLGGGGLGGGRGGYGGGGYGGGYGGGYGGGKYKG'

