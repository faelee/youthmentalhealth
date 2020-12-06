import csv
from collections import defaultdict

columns = defaultdict(list) # each value in each column is appended to a list
ac = set()
ap = set()
swc = set()
swp = set()

with open('ac.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        ac.add("" + row[6])

with open('ap.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        ap.add("" + row[7])

with open('swc.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        swc.add("" + row[6])

with open('swp.csv', 'rt') as csvfile:
    reader = csv.reader(csvfile) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        swp.add("" + row[7])

cp = ac & swp
cc = ac & swc
pp = ap & swp
pc = ap & swc

cp = sorted(cp)
cc = sorted(cc)
pp = sorted(pp)
pc = sorted(pc)
cc.remove('comment_username')
pp.remove('username')

with open('commonIDs.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
    writer.writerow(['User ID', 'Subreddit 1', 'Subreddit 2'])
    for value in cp:
        if value == '':
            writer.writerow(['[deleted]', 'Anxiety Commment', 'Suicide Watch Post'])
        else:
            writer.writerow(['' + value, 'Anxiety Comment', 'Suicide Watch Post'])
    for value in cc:
        if value == '':
            writer.writerow(['[deleted]', 'Anxiety Comment', 'Suicide Watch Comment'])
        else:
            writer.writerow(['' + value, 'Anxiety Comment', 'Suicide Watch Comment'])
    for value in pp:
        if value == '':
            writer.writerow(['[deleted]', 'Anxiety Post', 'Suicide Watch Post'])
        else:
            writer.writerow(['' + value, 'Anxiety Post', 'Suicide Watch Post'])
    for value in pc:
        if value == '':
            writer.writerow(['[deleted]' + value, 'Anxiety Post', 'Suicide Watch Comment'])
        else:
            writer.writerow(['' + value, 'Anxiety Post', 'Suicide Watch Comment'])