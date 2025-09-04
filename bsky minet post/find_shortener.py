from ural import get_domain_name
from tqdm import tqdm
import csv
from operator import itemgetter
from ural import is_shortened_url

file_path = "resolved_url_from_postbayrou.csv"

with open(file_path, 'r') as file:
    my_reader = csv.reader(file, delimiter=',')
    header = next(my_reader)
    links_id = header.index('link')
    resolved_links_id = header.index('resolved_url')
    domains = {}
    for row in (pbar := tqdm(my_reader)):
        original_url = row[links_id]
        resolved_url = row[resolved_links_id]
        original_domain_name = get_domain_name(original_url)
        resolved_domain_name = get_domain_name(resolved_url)
        if original_domain_name!=None and resolved_domain_name!=None:
            if original_domain_name!=resolved_domain_name:    
                if original_domain_name in domains.keys(): domains[original_domain_name][0]+=1
                else: domains[original_domain_name]=[1,0,0,0,original_url]
                if is_shortened_url(original_url): 
                    domains[original_domain_name][3]=1
                if len(original_url)<len(resolved_url):domains[original_domain_name][1]=1
                else:domains[original_domain_name][2]=1


    # keeping only susceptible new shorteners
    result = [[domain,domain_occur,shortener,redirect,already_in_ural,link] for domain, [domain_occur,shortener,redirect,already_in_ural,link] in domains.items() if shortener!=already_in_ural]
    result = [["domain","domain_occur","shortener","redirect","already_in_ural","link"]] + sorted(result, key=itemgetter(1))

    with open("most_probably_shortener_domains_from_"+file_path, 'w') as output:
        writer = csv.writer(output, delimiter=",")
        writer.writerows(result)