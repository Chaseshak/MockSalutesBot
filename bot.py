import praw
import config

reddit = praw.Reddit(user_agent="MockSaluteBot (by /u/chaseshak)",
                     client_id=config.clientID, client_secret=config.secretID,
                     username=config.uName, password=config.password)

subreddit = reddit.subreddit("HIMYM")

for submission in subreddit.hot(limit=5):
    print(submission)