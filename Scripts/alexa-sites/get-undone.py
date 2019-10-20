import csv

def read_csv(csvfilename):
    """
    Reads a csv file and returns a list of list
    containing rows in the csv file and its entries.
    """
    rows = []

    with open(csvfilename) as csvfile:
        file_reader = csv.reader(csvfile)
        for row in file_reader:
            rows.append(row)
    return rows

new_urls = read_csv('urls.csv')
old_urls = read_csv('finished-urls.csv')

done_domains = []

for i in old_urls:
    done_domains.append(i[1])

for j in new_urls:
    if j[1] not in done_domains:
        print(j[0] + "," + j[1] + "," + j[2] + "," + j[3])
   
