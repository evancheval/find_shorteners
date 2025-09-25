import csv
from shorteners_list import SHORTENER_DOMAINS as EXISTING_SHORTENER_DOMAINS
import argparse
import sys
import tempfile



parser = argparse.ArgumentParser(description="Extract URLs from posts CSV file.")
parser.add_argument("file_path", nargs="?", help="Path to the input CSV file (optional if using stdin)")
args = parser.parse_args()

if args.file_path:
    file_path = args.file_path
elif not sys.stdin.isatty():
    # Read from stdin and save to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, mode="w+", encoding="utf-8") as tmp:
        for line in sys.stdin:
            tmp.write(line)
        tmp.flush()
        file_path = tmp.name
else:
    parser.error("You must provide a file path or pipe data via stdin.")

with open(file_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        EXISTING_SHORTENER_DOMAINS.append(row['original_domain'])

EXISTING_SHORTENER_DOMAINS = list(set(EXISTING_SHORTENER_DOMAINS))

EXISTING_SHORTENER_DOMAINS.sort()

with open("updated_shorteners_list.py", "w", encoding="utf-8") as out_file:
    out_file.write("SHORTENER_DOMAINS = [\n")
    for domain in EXISTING_SHORTENER_DOMAINS:
        out_file.write(f"    \"{domain}\",\n")
    out_file.write("]\n")