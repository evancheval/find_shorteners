```bash
output=most_probably_shortener_domains.csv
xan select links "$file" | xan explode -D links | xan freq -s links -A | xan drop field | xan rename link -s value > temp-links.csv
minet resolve link -i temp-links.csv > not-temp-resolved-links.csv

minet url-parse link -i not-temp-resolved-links.csv | xan search -s probably_shortened no -e | xan select link,count,resolved_url,domain_name | xan rename original_domain -s domain_name | xan search -N -s original_domain > temp-original-domains.csv
minet url-parse resolved_url -i temp-original-domains.csv | xan select link,count,resolved_url,domain_name,original_domain | xan rename resolved_domain -s domain_name | xan search -N -s resolved_domain > temp-domains.csv
xan filter 'len(original_domain) < len(resolved_domain)' temp-domains.csv | xan groupby original_domain 'count(original_domain) as domain_occur' --keep link | xan rename example_link -s link | xan filter 'domain_occur > 5' | xan sort -NR -s domain_occur | xan map 'fmt("https://{}", original_domain) as domain_url' > "$output"
rm temp-*.csv
```

to retry the ones that failed with https status:

```bash
xan filter 'http_status not in [200, 202, 400, 401, 403, 404, 406, 410, 451, ""]' not-temp-resolved-links.csv | xan select link,count | minet resolve link -i - > not-temp-resolved-links-retry.csv
```

To see the most frequent probably shortened links that failed:

```bash
xan filter 'http_status not in [200, 202, 400, 401, 404, 406, 410, 451, ""]' not-temp-resolved-links.csv | xan select link,count | minet url-parse link -i - | xan search -s probably_shortened no -e | xan select link,count,domain_name | xan rename original_domain -s domain_name | xan search -N -s original_domain | xan groupby original_domain 'count(original_domain) as domain_occur' --keep link | xan rename example_link -s link | xan filter 'domain_occur > 5' | xan sort -NR -s domain_occur | xan map 'fmt("https://{}", original_domain) as domain_url' | xan v -pA
xan filter 'original_domain in ["ad.nl", "twp.ai", "h24.news", "u2m.io", "ara.tv", "7sur7.be", "tmt.news"]' | xan cat rows - "$output" > temp-new-output.csv
mv temp-new-output.csv "$output"
```

