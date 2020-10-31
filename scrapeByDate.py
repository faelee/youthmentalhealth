import json
import time
import math
import requests
import pandas as pd
import numpy as np
import praw

from datetime import datetime, timedelta


def give_me_intervals(start_at, number_of_days_per_interval=3):
    end_at = math.ceil(datetime.utcnow().timestamp())

    ## 1 day = 86400,
    period = (86400 * number_of_days_per_interval)

    end = start_at + period
    yield (int(start_at), int(end))

    padding = 1
    while end <= end_at:
        start_at = end + padding
        end = (start_at - padding) + period
        yield int(start_at), int(end)


def make_request(uri, max_retries=5):
    def fire_away(uri):
        response = requests.get(uri)
        assert response.status_code == 200
        return json.loads(response.content)

    current_tries = 1
    while current_tries < max_retries:
        try:
            response = fire_away(uri)
            return response
        except:
            time.sleep(.150)
            current_tries += 1

    return fire_away(uri)


def pull_posts_for(subreddit, start_at, end_at):
    def map_posts(posts):
        return list(map(lambda post: {
            'id': post['id'],
            'created_utc': post['created_utc'],
            'prefix': 't4_'
        }, posts))

    SIZE = 500
    URI_TEMPLATE = r'https://api.pushshift.io/reddit/search/submission?subreddit={}&after={}&before={}&size={}'

    post_collections = map_posts(make_request(URI_TEMPLATE.format(subreddit, start_at, end_at, SIZE))['data'])

    n = len(post_collections)
    while n == SIZE:
        last = post_collections[-1]
        new_start_at = last['created_utc'] - 10

        more_posts = map_posts(make_request(URI_TEMPLATE.format(subreddit, new_start_at, end_at, SIZE))['data'])

        n = len(more_posts)
        post_collections.extend(more_posts)

    return post_collections


end_at = math.ceil(datetime.utcnow().timestamp())

subreddit = 'SF9'

start_at = math.floor((datetime.utcnow() - timedelta(days=20)).timestamp())

posts = []
for interval in give_me_intervals(start_at, 7):
    pulled_posts = pull_posts_for(
        subreddit, interval[0], interval[1])

    posts.extend(pulled_posts)

print(posts)

posts_from_reddit = []

reddit = praw.Reddit(client_id="",#my client id
                     client_secret="",  #your client secret
                     user_agent="", #user agent name
                     username = "",     # your reddit username
                     password = "")

TIMEOUT_AFTER_COMMENT_IN_SECS = .250

for submission_id in np.unique([post['id'] for post in posts]):
    submission = reddit.submission(id=submission_id)

    posts_from_reddit.append(submission)

    submission.comments.replace_more(limit=None)

print(posts_from_reddit)

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
    topics_dict["username"].append(submission.author.name)
    topics_dict["body"].append(submission.selftext)

        ##### Acessing comments on the post
    submission.comments.replace_more(limit=None)
    for comment in submission.comments.list():
        comments_dict["comment_id"].append(comment.id)
        comments_dict["comment_parent_id"].append(comment.parent_id)
        comments_dict["comment_body"].append(comment.body)
        comments_dict["comment_link_id"].append(comment.link_id)
        comments_dict["comment_created"].append(comment.created)
        comments_dict["comment_username"].append(comment.author.name)


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
