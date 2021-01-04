import csv
import os

users = {}
subreddits = ["teenagers", "depression", "Anxiety", "SuicideWatch"]
file_name = "2020-1-1_2020-7-1.csv"
types = ['posts', 'comments']

for r in subreddits:
  for i in [0, 1]:
    with open(os.path.join("data", r, types[i], file_name), 'r') as file:
      reader = csv.reader(file)
      next(reader, None)
      for row in reader:
        username = row[7+i].strip ()
        if not username or username == '[deleted]':
          continue
        if username not in users:
          users[username] = {}
          for rr in subreddits:
            users[username][rr] = [0, 0]
          users[username]['total'] = [0, 0]
        users[username][r][i] += 1
        users[username]['total'][i] += 1

header = ['username', 'posted in teenagers and others', 'total post/comment number', 'total post number',
          'total comment number',
          'teenager posts',
          'teenager comments', 'depression posts', 'depression comments', 'anxiety posts', 'anxiety comments',
          'suicide watch posts', 'suicide watch comment']

with open ("stat.csv", "w") as csvfile:
  writer = csv.writer(csvfile)
  writer.writerow(header)
  for username in users:
    stat = users[username]
    row = [username, 'No', stat['total'][0] + stat['total'][1], stat['total'][0], stat['total'][1]]
    a = 0
    b = 0
    for r in subreddits:
      for i in [0, 1]:
        row.append (stat[r][i])
        if r == subreddits[0]:  # teeangers
          a += stat[r][i]
        else:
          b += stat[r][i]
    if a > 0 and b > 0:
      row[1] = "Yes"
    writer.writerow(row)
