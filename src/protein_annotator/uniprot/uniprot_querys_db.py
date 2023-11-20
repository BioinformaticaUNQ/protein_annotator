from Bio import SeqIO



def get_protein_db(uniprod_id, path_db, name_file_db)-> str:    
    uniprot = SeqIO.index(path_db, "swiss")
    with open(name_file_db, "wb") as out_handle:
        for acc in [uniprod_id]:
            print(acc)
            prot = uniprot.get_raw(acc)
            print(prot)
    return prot
            