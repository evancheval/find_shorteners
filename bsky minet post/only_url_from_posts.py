import csv
import argparse

parser = argparse.ArgumentParser(description="Extract URLs from posts CSV file.")
parser.add_argument("file_path", help="Path to the input CSV file")
args = parser.parse_args()
file_path = args.file_path

with open(file_path, "r") as file:
    my_reader = csv.reader(file, delimiter=",")
    header = next(my_reader)
    links_id = header.index("links")
    user_handle_id = header.index("user_handle")
    result = [["link", "occur"]]
    links_dic = {}
    max_occur = 0
    for row in my_reader:
        if row[links_id] != "":
            for url in row[links_id].split(
                "|"
            ):  # séparer les liens quand il y en a plusieurs dans le même post
                # if url in links_dic:
                #     links_dic[url] += 1
                # else:
                #     links_dic[url] = 1
                links_dic[url] = links_dic.get(url, 0) + 1
                max_occur = max(max_occur, links_dic[url])

    result += [[url, occur] for url, occur in links_dic.items()]

with open("extracted_url_from_" + file_path, "w") as output:
    writer = csv.writer(output, delimiter=",")
    writer.writerows(result)
