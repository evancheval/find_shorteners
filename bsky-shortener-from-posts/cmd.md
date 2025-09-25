Privilégier l'utilisation de xan !!!!!



```bash
output=most_probably_shortener_domains.csv
python only_url_from_posts.py "$file" > temp.csv
minet resolve link -i temp.csv | python find_shortener.py > "$output"
rm temp.csv
xan filter 'is_shortener==1 and is_already_in_ural==0' "$output" | xan v -pA -s domain,domain_occur,link
```