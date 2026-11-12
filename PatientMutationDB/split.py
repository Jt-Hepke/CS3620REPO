import csv
import re
import sys
import pandas as pd

SPREADSHEET = sys.argv[1] if len(sys.argv) > 1 else "mutationu.xlsx"
FIRST_MID = 0  #First mid

HEADER = re.compile(r"^(.+?)_(GRCh3\d)_([^:]+):(\d+)-(\d+)_(.+?)_([A-Z]+)_(.+)$")

def patient_order(pid):
    """Sort key: C0, C1, ... C105 first, then NC0, NC1, ... NC135."""
    number = int(pid.lstrip("NC"))
    return (pid.startswith("NC"), number)

def write_csv(filename, rows):
    with open(filename, "w", newline="") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)
    print(f"{filename}: {len(rows)} rows")

sheet = pd.read_excel(SPREADSHEET, header=0, index_col=0)

patients = {}          # pid -> cancer_status (1 or 0)
genes = {}             # gene_name -> chromosome
mutations = []         # (mid, gene_name, mutation_type, poly_type, start, end, start_nucleotide)
end_nucleotides = []   # (mid, nucleotide)
has_mutation = []      # (pid, mid)

for pid in sheet.index:
    patients[pid] = 0 if pid.startswith("NC") else 1

for mid, header in enumerate(sheet.columns, start=FIRST_MID):
    match = HEADER.match(header)
    if match is None:
        raise ValueError(f"Unexpected column header: {header}")
    gene, build, chromosome, start, end, mut_type, poly_type, nucleotides = match.groups()

    genes[gene] = chromosome

    variants = nucleotides.split("_")
    start_nucleotide = variants[0].split("-")[0] or "-"

    mutations.append((mid, gene, mut_type, poly_type, int(start), int(end), start_nucleotide))

    seen = []
    for variant in variants:
        end_match = re.match(r"^(?:[ACGT]+|-)-(?:[ACGT]+|-)-([ACGT]+|-)$", variant)
        if end_match is None:
            raise ValueError(f"Unexpected nucleotide pattern: {variant}")
        end_nucleotide = end_match.group(1)
        if end_nucleotide not in seen:
            seen.append(end_nucleotide)
    for nuc in seen:
        end_nucleotides.append((mid, nuc))

    for pid in sheet.index[sheet[header] == 1]:
        has_mutation.append((pid, mid))

write_csv("patient.csv",        sorted(patients.items(), key=lambda row: patient_order(row[0])))
write_csv("gene.csv",           sorted(genes.items()))
write_csv("mutation.csv",       mutations)
write_csv("has_mutation.csv",   sorted(has_mutation, key=lambda row: (patient_order(row[0]), row[1])))
write_csv("end_nucleotide.csv", sorted(end_nucleotides))