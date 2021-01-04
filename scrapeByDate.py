import json
import requests
import praw
import prawcore
import time
import os
import traceback
import sys
import csv

from datetime import datetime, timezone
import pprint

pp = pprint.PrettyPrinter(indent=2)


# Check server rate limit
# https://api.pushshift.io/meta
# Key: server_ratelimit_per_minute

def getPushshiftData(after, before, sub):
    while True:
      url = 'https://api.pushshift.io/reddit/search/submission/?size=1000&after=' + str(after) + '&before=' + str(before)\
            + '&subreddit='+str(sub)
      print(url)
      r = requests.get(url)
      try:
        data = json.loads(r.text)
        return data['data']
      except:
        print ("Hit limit. Wait for 1 second.")
        time.sleep (0.5)


def collectSubData(subm):
    subData = list()  # list to store data points
    sub_id = subm['id']
    created = datetime.fromtimestamp(subm['created_utc'])  # 1520561700.0

    subData.append((sub_id, created))
    subStats[sub_id] = subData


def get_date(created):
    return datetime.fromtimestamp(created)


if len (sys.argv) < 8:
    print ("Usage: {} start_year start_month start_day end_year end_month end_day subreddit [begin timestamp]".format (sys.argv[0]))
    quit ()


#Subreddit to query
# subreddit= input("Subreddit Name (ex. for the Subreddit r/NFlying type NFlying): ")
subreddit = sys.argv[7]

#before and after dates
# yearB = int(input("Year of Start Date (4 digits): "))
# monthB = int(input("Month of Start Date (2 digits): "))
# dayB = int(input("Day of Start Date (2 digits): "))
yearB = int (sys.argv[1])
monthB =  int (sys.argv[2])
dayB = int (sys.argv[3])
dtB = datetime(yearB, monthB, dayB, tzinfo=timezone.utc)
after = str(int(dtB.timestamp()))

# yearA = int(input("Year of End Date (4 digits): "))
# monthA = int(input("Month of End Date (2 digits): "))
# dayA = int(input("Day of End Date (2 digits): "))
yearA = int (sys.argv[4])
monthA =  int (sys.argv[5])
dayA = int (sys.argv[6])
dtA = datetime(yearA, monthA, dayA, tzinfo=timezone.utc)
before = str(int(dtA.timestamp()))

if len(sys.argv) > 8:
  after = sys.argv[8]
  csv_header = False
else:
  csv_header = True

path_suffix = "{}-{}-{}_{}-{}-{}".format (yearB, monthB, dayB, yearA, monthA, dayA)

print(before)
print(after)

subStats = {}

# reddit = praw.Reddit(client_id="NR9oyISKuXum1A",#my client id
#                     client_secret="Fp-ceh8LbTC8VsaRQF4hZtWg4z4",  #your client secret
#                     user_agent="covid_research", #user agent name
#                     username = "smoolsheep",     # your reddit username
#                     password = "illbeyourhome")
reddit = praw.Reddit(client_id="JJHRTUklGCcjgA",#my client id
                     client_secret="0FUN6GCDISZyeyphy5qYeyCbiL6K4w",  #your client secret
                     user_agent="Mental health research", #user agent name
                     username = "xyjadm",     # your reddit username
                     password = "24689yhnjm")

TIMEOUT_AFTER_COMMENT_IN_SECS = .250

post_header = [
    "number",
    "title",
    "score",
    "id",
    "url",
    "comms_num",
    "created_utc",
    "username",
#    "user_id",
    "body"
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
    "comment_username"
#    "comment_user_id"
]
total = 0
comment_total = 0
start_time = datetime.now ()

path_prefix = os.path.join ("data", subreddit)
if not os.path.isdir(path_prefix):
    os.makedirs(path_prefix)
for t in ["comments", "posts"]:
    if not os.path.isdir(os.path.join (path_prefix, t)):
        os.makedirs(os.path.join (path_prefix, t))

data = getPushshiftData(after, before, subreddit)
# Will run until all posts have been gathered
# from the 'after' date up until before date
while len(data) > 0:
  try:
    post_lazy_list = []
    for submission in data:
        collectSubData(submission)
        submission_id = submission['id']
        subm = reddit.submission(id=submission_id)
        post_lazy_list.append (subm)

    while True:
      topic_dict_list = []
      comment_dict_list = []
      temp_post_total = total
      temp_comment_total = comment_total
      try:
          for submission in post_lazy_list:
              try:
                topic_dict = {}
                subm_copy = str (submission)
                topic_dict["title"] = submission.title
                topic_dict["score"] = submission.score
                topic_dict["id"] = submission.id
                topic_dict["url"] = submission.url
                topic_dict["comms_num"] = submission.num_comments
                topic_dict["created_utc"] = submission.created_utc
                topic_dict["username"] = submission.author
                topic_dict["body"] = submission.selftext
                temp_post_total +=1
                topic_dict["number"] = temp_post_total
                topic_dict_list.append (topic_dict)

                ##### Acessing comments on the post
                submission.comments.replace_more(limit=None)

                for comment in submission.comments.list():
                    temp_comment_total += 1
                    comment_dict = {}
                    comment_dict["number"] = temp_comment_total
                    comment_dict["post_id"] = submission.id
                    comment_dict["post_id_2"] = comment.link_id
                    comment_dict["comment_id"] = comment.id
                    comment_dict["comment_parent_id"] = comment.parent_id
                    comment_dict["comment_body"] = comment.body
                    comment_dict["comment_link_id"] = comment.link_id
                    comment_dict["comment_created_utc"] = comment.created_utc
                    comment_dict["comment_username"] = comment.author
                    comment_dict_list.append (comment_dict)
              except prawcore.exceptions.NotFound:
                sys.stderr.write("Not found: %s\n" % subm_copy)
              except AssertionError:
                sys.stderr.write("Rate limit: %s\n" % subm_copy)


              # pp.pprint (topic_dict)
              if temp_post_total % 10 == 0:
                  time_delta = (datetime.now () - start_time).total_seconds ()
                  print ("Total {} in {} sec, avg one per {:.2f} sec".format(temp_post_total, time_delta, time_delta / temp_post_total))
          break
      except:
          traceback.print_exc()
          print ("Exception. Wait for 2 sec.")
          time.sleep (2)

    total = temp_post_total
    comment_total = temp_comment_total

    try:
        with open (os.path.join (path_prefix, "comments", path_suffix + ".csv"), "a") as comment_file:
            writer = csv.DictWriter(comment_file, fieldnames=comment_header)
            if csv_header:
                writer.writeheader()
            for d in comment_dict_list:
                writer.writerow(d)

        with open (os.path.join (path_prefix, "posts", path_suffix + ".csv"), "a") as post_file:
            writer = csv.DictWriter(post_file, fieldnames=post_header)
            if csv_header:
                writer.writeheader()
            for d in topic_dict_list:
                writer.writerow(d)
    except IOError:
        traceback.print_exc()
        quit ()

    csv_header = False

    # Calls getPushshiftData() with the created date of the last submission
    print(len(data))
    print(str(datetime.fromtimestamp(data[0]['created_utc'])))
    print(str(datetime.fromtimestamp(data[len(data) - 1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushshiftData(after, before, subreddit)
    time.sleep (0.5)
  except KeyboardInterrupt:
    sys.exit ()
