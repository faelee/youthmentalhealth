import json
import requests
import pandas as pd
import praw
import time
import os
import traceback

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


def get_date(created):
    return datetime.fromtimestamp(created)


#Subreddit to query
# subreddit= input("Subreddit Name (ex. for the Subreddit r/NFlying type NFlying): ")
subreddit = "teenagers"

#before and after dates
# yearB = int(input("Year of Start Date (4 digits): "))
# monthB = int(input("Month of Start Date (2 digits): "))
# dayB = int(input("Day of Start Date (2 digits): "))
yearB = 2019
monthB =  1
dayB = 1
dtB = datetime(yearB, monthB, dayB, tzinfo=timezone.utc)
after = str(int(dtB.timestamp()))

# yearA = int(input("Year of End Date (4 digits): "))
# monthA = int(input("Month of End Date (2 digits): "))
# dayA = int(input("Day of End Date (2 digits): "))
yearA = 2020
monthA = 10
dayA = 31
dtA = datetime(yearA, monthA, dayA, tzinfo=timezone.utc)
before = str(int(dtA.timestamp()))

print(before)
print(after)

reddit = praw.Reddit(client_id="",#my client id
                     client_secret="",  #your client secret
                     user_agent="", #user agent name
                     username = "",     # your reddit username
                     password = "")

TIMEOUT_AFTER_COMMENT_IN_SECS = .250

topics_dict_empty = {
    "title": [],
    "score": [],
    "id": [],
    "url": [],
    "comms_num": [],
    "created": [],
    "username": [],
    "body": []
}
comments_dict_empty = {
    "comment_id": [],
    "comment_parent_id": [],
    "comment_body": [],
    "comment_link_id": [],
    "comment_created": [],
    "comment_username": []
}
csv_header = True
total = 0
subtotal = 0
start_time = datetime.now ()

data = getPushshiftData(after, before, subreddit)
# Will run until all posts have been gathered
# from the 'after' date up until before date
while len(data) > 0:
    post_lazy_list = []
    for subm in data:
        submission_id = subm['id']
        submission = reddit.submission(id=submission_id)
        post_lazy_list.append (submission)

    while True:
      topic_dict = topics_dict_empty
      comment_dict = comments_dict_empty
      try:
          for submission in post_lazy_list:
              topic_dict["title"].append (submission.title)
              topic_dict["score"].append (submission.score)
              topic_dict["id"].append (submission.id)
              topic_dict["url"].append (submission.url)
              topic_dict["comms_num"].append (submission.num_comments)
              topic_dict["created"].append (submission.created)
              topic_dict["username"].append (submission.author)
              topic_dict["body"].append (submission.selftext)

              ##### Acessing comments on the post
              submission.comments.replace_more(limit=None)

              for comment in submission.comments.list():
                  comment_dict["comment_id"].append(comment.id)
                  comment_dict["comment_parent_id"].append(comment.parent_id)
                  comment_dict["comment_body"].append(comment.body)
                  comment_dict["comment_link_id"].append(comment.link_id)
                  comment_dict["comment_created"].append(comment.created)
                  comment_dict["comment_username"].append(comment.author)

              # pp.pprint (topic_dict)
              total += 1
              if total % 10 == 0:
                  time_delta = (datetime.now () - start_time).total_seconds ()
                  print ("Total {} in {} sec, avg one per {:.2f} sec".format(total, time_delta, time_delta / total))
          break
      except:
          traceback.print_exc()
          print ("Exception. Wait for 2 sec.")
          time.sleep (2)

    post_comments = pd.DataFrame(comment_dict)
    ttimestamp = post_comments["comment_created"].apply(get_date)
    post_comments = post_comments.assign(timestamp=ttimestamp)
    post_comments.to_csv("data/" + subreddit + "_comments_subreddit.csv", mode = "a", header = csv_header)

    post_data = pd.DataFrame(topic_dict)
    _timestamp = post_data["created"].apply(get_date)
    post_data = post_data.assign(timestamp=_timestamp)
    post_data.to_csv("data/" + subreddit + "_subreddit.csv", mode = "a", header = csv_header)

    csv_header = False

    # Calls getPushshiftData() with the created date of the last submission
    print(len(data))
    print(str(datetime.fromtimestamp(data[0]['created_utc'])))
    print(str(datetime.fromtimestamp(data[len(data) - 1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushshiftData(after, before, subreddit)
    time.sleep (0.5)
