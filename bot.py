import praw
import config


words = ["major", "colonel", "kernel", "general", "private"]
mapping = {
    'major': 'Major',
    'colonel': 'Colonel',
    'kernel': 'Colonel',
    'general': 'General',
    'private': 'Private'
}


reddit = praw.Reddit(user_agent="MockSaluteBot (by /u/chaseshak)",
                     client_id=config.clientID, client_secret=config.secretID,
                     username=config.uName, password=config.password)

# Set to /r/HIMYM for least likely to be banned for many comments
subreddit = reddit.subreddit("HIMYM")


def reply_to_comment(comment, word, to_reply):

    # Safety check the to_reply word for any odd characters
    # TODO

    mock_salute = mapping[word] + " " + to_reply.title()

    print("Salute: " + mock_salute)

    # print("Comment: " + str(comment) + " word: " + word + " reply: " + mapping[word] + " " + to_reply)
    return


def check_body(comment):
    # Check for 'MoreComments' object and break it down into Comment objects
    # Recursively calls check_body function
    if isinstance(comment, praw.models.reddit.more.MoreComments):
        more_comments = comment.comments()
        for comment in more_comments:
            check_body(comment)
        return

    # If not a 'MoreComment' check the body for one of the key words
    body = comment.body.lower()
    for word in words:
        index = body.find(word)
        if index != -1:
            # Split the string by spaces
            tokens = body.split()
            # Check for exact instances of the word, if no exact instances, continue
            # (Prevents things such as 'majorly' or 'generally' from triggering reply
            try:
                index_word = tokens.index(word)
            except ValueError:
                continue

            # Only get next word if not end of array
            if index_word != (len(tokens) - 1):
                reply_to_comment(comment, word, tokens[index_word + 1])


for submission in subreddit.hot(limit=10):
    comments = submission.comments.list()
    for comment in comments:
        check_body(comment)

