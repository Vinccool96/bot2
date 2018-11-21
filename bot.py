import configparser
import combinations

import praw
from prawcore import NotFound, Forbidden

conf = configparser.ConfigParser()
conf.read('praw.ini')


def sub_exists(subre):
    exists = True
    try:
        reddit.subreddits.search_by_name(subre, exact=True)
    except NotFound:
        exists = False
    return exists


characs = '0123456789abcdefghijklmnopqrstuvwxyz-_'

reddit = praw.Reddit(client_id=conf.get('Bot2', 'client_id'), client_secret=conf.get('Bot2', 'client_secret'),
                     user_agent=conf.get('Bot2', 'user_agent'), password=conf.get('Bot2', 'password'),
                     username=conf.get('Bot2', 'username'))

names = combinations.comb_ordr_rep__of_len_in_range_str(characs, 3, 4)

print('combinations done', len(names))

fil = open('subreddits3chars.txt', 'a')

for sub in names:
    try:
        fil.write(sub+' is NSFW: ' + str(reddit.subreddit(sub).over18) + '\n')
        print(sub+' is NSFW: ' + str(reddit.subreddit(sub).over18))
    except Forbidden:
        pass
    except NotFound:
        pass
    except Exception:
        pass

print('\ndone')
