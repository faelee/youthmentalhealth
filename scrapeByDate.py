import json
import requests
import pandas as pd
import praw

from datetime import datetime, timezone


def getPushshiftData(after, before, sub):
    url = 'https://api.pushshift.io/reddit/search/submission/?size=1000&after=' + str(after) + '&before=' + str(before)\
          + '&subreddit='+str(sub)
    print(url)
    r = requests.get(url)
    data = json.loads(r.text)
    return data['data']


def collectSubData(subm):
    subData = list()  # list to store data points
    sub_id = subm['id']
    created = datetime.fromtimestamp(subm['created_utc'])  # 1520561700.0

    subData.append((sub_id, created))
    subStats[sub_id] = subData

#Subreddit to query
subreddit= input("Subreddit Name (ex. for the Subreddit r/NFlying type NFlying): ")

#before and after dates
yearB = int(input("Year of Start Date (4 digits): "))
monthB = int(input("Month of Start Date (2 digits): "))
dayB = int(input("Day of Start Date (2 digits): "))
dtB = datetime(yearB, monthB, dayB)
after = str(int(dtB.replace(tzinfo=timezone.utc).timestamp()))

yearA = int(input("Year of End Date (4 digits): "))
monthA = int(input("Month of End Date (2 digits): "))
dayA = int(input("Day of End Date (2 digits): "))
dtA = datetime(yearA, monthA, dayA)
before = str(int(dtA.replace(tzinfo=timezone.utc).timestamp()))

print(before)
print(after)

subCount = 0
subStats = {}
posts_from_reddit = []
#comments_from_reddit = []

reddit = praw.Reddit(client_id="NR9oyISKuXum1A",#my client id
                     client_secret="Fp-ceh8LbTC8VsaRQF4hZtWg4z4",  #your client secret
                     user_agent="covid_research", #user agent name
                     username = "smoolsheep",     # your reddit username
                     password = "illbeyourhome")

TIMEOUT_AFTER_COMMENT_IN_SECS = .250

data = getPushshiftData(after, before, subreddit)
# Will run until all posts have been gathered
# from the 'after' date up until before date
while len(data) > 0:
    for submission in data:
        collectSubData(submission)
        submission_id = submission['id']
        subm = reddit.submission(id=submission_id)
        posts_from_reddit.append(subm)
        subCount += 1
    # Calls getPushshiftData() with the created date of the last submission
    print(len(data))
    print(str(datetime.fromtimestamp(data[len(data) - 1]['created_utc'])))
    after = data[-1]['created_utc']
    data = getPushshiftData(after, before, subreddit)

print(len(data))

topics_dict = {
    "title": [],
    "score": [],
    "id": [],
    "url": [],
    "comms_num": [],
    "created": [],
    "username": [],
    "body": []
}
comments_dict = {
    "comment_id": [],
    "comment_parent_id": [],
    "comment_body": [],
    "comment_link_id": [],
    "comment_created": [],
    "comment_username": []
}
for submission in posts_from_reddit:
    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(submission.created)
    topics_dict["username"].append(submission.author)
    topics_dict["body"].append(submission.selftext)

        ##### Acessing comments on the post
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        comments_dict["comment_id"].append(comment.id)
        comments_dict["comment_parent_id"].append(comment.parent_id)
        comments_dict["comment_body"].append(comment.body)
        comments_dict["comment_link_id"].append(comment.link_id)
        comments_dict["comment_created"].append(comment.created)
        comments_dict["comment_username"].append(comment.author)


def get_date(created):
    return datetime.fromtimestamp(created)


post_comments = pd.DataFrame(comments_dict)
ttimestamp = post_comments["comment_created"].apply(get_date)
post_comments = post_comments.assign(timestamp=ttimestamp)
post_comments.to_csv(subreddit + "_comments_subreddit.csv")

post_data = pd.DataFrame(topics_dict)
_timestamp = post_data["created"].apply(get_date)
post_data = post_data.assign(timestamp=_timestamp)
post_data.to_csv(subreddit + "_subreddit.csv")
