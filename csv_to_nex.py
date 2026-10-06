import csv
import sys
from pathlib import Path

def pham_key(pham):
    try:
        return (0, int(pham), pham)
    except ValueError:
        return (1, 0, pham)

def quote(name):
    return "'" + name.replace("'", "''") + "'"

def convert(input_file, output_file):
    phage_phams = {}
    all_phams = set()

    with input_file.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, strict=True)
        columns = reader.fieldnames or []
        if "PhageID" not in columns or "PhamID" not in columns:
            raise ValueError("CSV needs PhageID and PhamID columns")

        for row in reader:
            phage = (row["PhageID"] or "").strip()
            pham = (row["PhamID"] or "").strip()
            if not phage or not pham:
                continue
            if phage not in phage_phams:
                phage_phams[phage] = set()
            phage_phams[phage].add(pham)
            all_phams.add(pham)

    if not phage_phams:
        raise ValueError("No phage/pham pairs")

    phages = sorted(phage_phams)
    phams = sorted(all_phams, key=pham_key)

    with output_file.open("w", encoding="utf-8") as f:
        f.write("#NEXUS\n\nBEGIN TAXA;\n")
        f.write(f"    DIMENSIONS NTAX={len(phages)};\n    TAXLABELS\n")
        for phage in phages:
            f.write(f"        {quote(phage)}\n")
        f.write("    ;\nEND;\n\nBEGIN CHARACTERS;\n")
        f.write(f"    DIMENSIONS NCHAR={len(phams)};\n")
        f.write('    FORMAT DATATYPE=STANDARD SYMBOLS="01" GAP=- MISSING=?;\n')
        f.write("    CHARLABELS " + " ".join(quote(pham) for pham in phams) + ";\n")
        f.write("    MATRIX\n")
        for phage in phages:
            sequence = "".join("1" if pham in phage_phams[phage] else "0" for pham in phams)
            f.write(f"        {quote(phage)}  {sequence}\n")
        f.write("    ;\nEND;\n")

    print(f"Created: {output_file}")
    print(f"Phages: {len(phages)}")
    print(f"Unique phams: {len(phams)}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Format: python3 csv_to_nex.py INPUT_NAME.csv OUTPUT_NAME.nex")

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    convert(input_file, output_file)
