import csv
import os
import text2emotion as te

teen_dict = {}

with open("stat.csv", 'r') as in_file:
  reader = csv.reader(in_file)
  next(reader, None)
  for row in reader:
    if row[1] == "Yes":
      teen_dict[row[0]] = 1


subreddits = ["teenagers", "depression", "Anxiety", "SuicideWatch"]
file_name = "2020-1-1_2020-7-1.csv"
emotion_file_name = "2020-1-1_2020-7-1.emotion.csv"
types = ['posts', 'comments']

post_header = [
    "number",
    "title",
    "score",
    "id",
    "url",
    "comms_num",
    "created_utc",
    "username",
    "body",
    'Angry', 'Fear', 'Happy', 'Sad', 'Surprise'
 ]
comment_header = [
    "number",
    "post_id",
    "post_id_2",
    "comment_id",
    "comment_parent_id",
    "comment_body",
    "comment_link_id",
    "comment_created_utc",
    "comment_username",
    'Angry', 'Fear', 'Happy', 'Sad', 'Surprise'
]


for r in subreddits:
  for i in [0, 1]:
    with open(os.path.join("data", r, types[i], file_name), 'r') as in_file,\
        open(os.path.join("data", r, types[i], emotion_file_name), 'w') as out_file:
      reader = csv.reader(in_file)
      next(reader, None)
      writer = csv.writer(out_file)
      if i == 0:
        writer.writerow(post_header)
      else:
        writer.writerow(comment_header)
      for row in reader:
        if r != "teenagers" and row[7+i].strip () not in teen_dict:
          continue
        if i == 0:
          text = row[1].strip () + "\n" + row[8].strip ()
          if text == "\n":
            continue
        else:
          text = row[5].strip()
          if not text:
            continue
        emot = te.get_emotion(text)
        row.extend([emot['Angry'], emot['Fear'], emot['Happy'], emot['Sad'], emot['Surprise']])
        writer.writerow(row)
        print ("{} {}: {}".format (r, types[i], row[0]))
