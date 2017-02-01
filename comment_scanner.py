# This py script scans /r/all periodically (Once every 2 hours executed by crontab)
# and imports the comments to reply to in a database
# To see what happens once a row is in the DB, see comment_reply.py
import praw
import config


words = ["major", "colonel", "kernel", "general", "corporal"]
mapping = {
    'major': 'Major',
    'colonel': 'Colonel',
    'kernel': 'Colonel',
    'general': 'General',
    'corporal': 'Corporal'
}


reddit = praw.Reddit(user_agent="MockSaluteBot (by /u/chaseshak)",
                     client_id=config.clientID, client_secret=config.secretID,
                     username=config.uName, password=config.password)

# Set to /r/HIMYM for least likely to be banned for many comments
subreddit = reddit.subreddit("all")


def reply_to_comment(comment, word, to_reply):

    # Safety check the to_reply word for any odd characters
    to_reply = to_reply.translate({ord(i): None for i in '!@#$\".'})

    # Create the mock salute
    mock_salute = mapping[word] + " " + to_reply.title() + "!" + " (｀-´)>"

    # Formatted comment reply for Reddit
    comment_reply = mock_salute + "  \n&nbsp;  \n^(I am a bot. Mock Salutes are a joke from) " \
                                  "[^HIMYM](http://how-i-met-your-mother.wikia.com/wiki/Mock_Salutes)^. ^( This"\
                                  " comment was auto-generated. To learn more " \
                                  "about me, see my) [^github ^page](https://github.com/Chaseshak/MockSalutesBot)^."

    print(comment_reply)

    # Insert into DB
    # comment.reply(comment_reply)

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


for submission in subreddit.hot(limit=20):
    comments = submission.comments.list()
    for comment in comments:
        check_body(comment)

