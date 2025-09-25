import argparse
import sys
from ural import get_domain_name
from tqdm import tqdm
import csv
from operator import itemgetter
from ural import is_shortened_url
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

result = [
    [
        "domain",
        "domain_occur",
        "is_shortener",
        "is_redirect",
        "is_already_in_ural",
        "link",
    ]
]

with open(file_path, "r") as file:
    my_reader = csv.reader(file, delimiter=",")
    header = next(my_reader)
    links_id = header.index("link")
    resolved_links_id = header.index("resolved_url")
    occur_id = header.index("occur")
    domains = {}
    for row in (pbar := tqdm(my_reader)):
        original_url = row[links_id]
        resolved_url = row[resolved_links_id]
        occur = int(row[occur_id])
        original_domain_name = get_domain_name(original_url)
        resolved_domain_name = get_domain_name(resolved_url)
        if original_domain_name is not None and resolved_domain_name is not None:
            if original_domain_name != resolved_domain_name:
                if original_domain_name in domains.keys():
                    domains[original_domain_name]["domain_occur"] += occur
                else:
                    domains[original_domain_name] = {
                        "domain_occur": occur,
                        "is_shortener": 0,
                        "is_redirect": 0,
                        "is_already_in_ural": 0,
                        "link": original_url,
                    }
                if is_shortened_url(original_url):
                    domains[original_domain_name]["is_already_in_ural"] = 1
                if len(original_url) < len(resolved_url):
                    domains[original_domain_name]["is_shortener"] = 1
                else:
                    domains[original_domain_name]["is_redirect"] = 1

    # keeping only susceptible new shorteners
    result += sorted(
        [
            [
                domain,
                domain_info["domain_occur"],
                domain_info["is_shortener"],
                domain_info["is_redirect"],
                domain_info["is_already_in_ural"],
                domain_info["link"],
            ]
            for domain, domain_info in domains.items()
        ],
        key=itemgetter(1),
        reverse=True,
    )

writer = csv.writer(sys.stdout, delimiter=",")
writer.writerows(result)
