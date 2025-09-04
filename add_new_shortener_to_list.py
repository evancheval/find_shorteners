import csv

SHORTENER_DOMAINS = [] # e.g. ['bit.ly', 't.co', ...

with open("most_probably_shortener_domains_from_resolved_url_from_postbayrou.csv", 'r') as f:
    my_reader=csv.reader(f)
    next(my_reader)  # skip header
    for row in my_reader:
        SHORTENER_DOMAINS.append(row[0])

SHORTENER_DOMAINS.sort()

# print(SHORTENER_DOMAINS)