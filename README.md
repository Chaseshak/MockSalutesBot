# MockSalutesBot
***Requires python3***
 
 The source code repository for a Python reddit bot that crawls comments. If the bot finds a comment such as 'Major', 'Captain', 'General', 'Kernel' (pronunciation) and replies with that title and the following word.

Before using this bot, please read through [Reddit's Bottiquette](https://www.reddit.com/wiki/bottiquette) and be aware that moderators of subreddits you comment on reserve the right to ban you.


## Required Dependencies
This script requires the following dependencies:
- [PRAW Python Reddit API Wrapper](https://praw.readthedocs.io/en/latest/getting_started/quick_start.html)
    - Install with pip: `pip install praw`

- [peewee](http://peewee.readthedocs.io/en/latest/peewee/quickstart.html) simply python ORM
    - Install with pip: `pip install peewee`

- [PyMySQL](https://github.com/PyMySQL/PyMySQL) Dependency of `peewee` for MySQL Connector
     - Install with pip: `pip install PyMySQL`

## Configuration
If you wish to use the bot, please download the source code and copy the contents of `config.template.py` into `config.py` using your reddit app credentials and your database credentials.
