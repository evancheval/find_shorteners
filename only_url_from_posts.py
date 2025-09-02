import csv

file_path = "postbayrou.csv" # csv result from minet request

with open(file_path, 'r') as file:
    my_reader = csv.reader(file, delimiter=',')
    header = next(my_reader)
    links_id = header.index('links')
    user_handle_id = header.index('user_handle')
    result = [['link','occur']]
    links_dic={}
    max_occur = 0
    for row in my_reader:
        if row[links_id]!="":
            for url in row[links_id].split('|'): #séparer les liens quand il y en a plusieurs dans le même post
                if url in links_dic.keys(): links_dic[url]+=1
                else: links_dic[url]=1
                max_occur = max(max_occur,links_dic[url])

    result += [[url,occur] for url, occur in links_dic.items()]

    with open("extracted_url_from_"+file_path, 'w') as output:
        writer = csv.writer(output, delimiter=",")
        writer.writerows(result)