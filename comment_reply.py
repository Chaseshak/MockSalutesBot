import praw
import config
import peewee
import prawcore


# DB Connection for peewee using config values
db = peewee.MySQLDatabase(config.db_name, user=config.db_user, password=config.db_pass, host=config.db_host)


# Define comment table class
class PendingComments(peewee.Model):
    comment_id = peewee.TextField()
    salute = peewee.TextField()

    class Meta:
        database = db


# Connect to Reddit
reddit = praw.Reddit(user_agent="Mock_Salute_Bot (by /u/chaseshak)",
                     client_id=config.clientID, client_secret=config.secretID,
                     username=config.uName, password=config.password)


# Placed in function so it can call itself in case comment fails to post
# This way it can move onto the next comment
def reply_to_comment():

    # Get the first comment pending in the db
    comment_sql = PendingComments.get()

    # Create the comment PRAW object
    comment = reddit.comment(comment_sql.comment_id)

    # Formatted comment reply for Reddit
    comment_reply = comment_sql.salute + "  \n&nbsp;  \n^(I am a bot. Mock Salutes are a joke from) "\
                                  "[^HIMYM](http://how-i-met-your-mother.wikia.com/wiki/Mock_Salutes)^. ^( This"\
                                  " comment was auto-generated. To learn more " \
                                  "about me, see my) [^github ^page](https://github.com/Chaseshak/MockSalutesBot)^."
    # Reply to the comment
    try:
        comment.reply(comment_reply)
    except prawcore.exceptions.Forbidden as e:
        # Remove the row and try the next
        comment_sql.delete_instance()
        reply_to_comment()
        return
    except praw.exceptions.APIException as e2:
        # Remove the row and try the next
        comment_sql.delete_instance()
        reply_to_comment()
        return

    # Delete the DB row
    comment_sql.delete_instance()


# First call to reply function
reply_to_comment()
