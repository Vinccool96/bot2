import configparser
import combinations

import praw
from prawcore import NotFound, Forbidden

conf = configparser.ConfigParser()
conf.read('praw.ini')


def sub_exists(sub):
    exists = True
    try:
        reddit.subreddits.search_by_name(sub, exact=True)
    except NotFound:
        exists = False
    return exists


dict = '0123456789abcdefghijklmnopqrstuvwxyz-_'

reddit = praw.Reddit(client_id=conf.get('Bot2', 'client_id'), client_secret=conf.get('Bot2', 'client_secret'),
                     user_agent=conf.get('Bot2', 'user_agent'), password=conf.get('Bot2', 'password'),
                     username=conf.get('Bot2', 'username'))

names = combinations.comb_ordr_rep__of_len_in_range_str(dict, 3, 5)

print('combinations done', len(names))

fil = open('subreddits.txt', 'a')

for sub in names:
    try:
        if sub_exists(sub):
            fil.write(sub+' is NSFW: ' + str(reddit.subreddit(sub).over18))
            print(sub+' is NSFW: ' + str(reddit.subreddit(sub).over18))
    except Forbidden:
        pass
    except NotFound:
        pass

print('\ndone')
