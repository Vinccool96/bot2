import configparser
import combinations
import requests
import json

import praw
from prawcore import NotFound, Forbidden

conf = configparser.ConfigParser()
conf.read('praw.ini')


# def sub_exists(subre):
#     exists = True
#     try:
#         reddit.subreddits.search_by_name(subre, exact=True)
#     except NotFound:
#         exists = False
#     return exists
#
#
# characs = '0123456789abcdefghijklmnopqrstuvwxyz-_'
#
# reddit = praw.Reddit(client_id=conf.get('Bot2', 'client_id'), client_secret=conf.get('Bot2', 'client_secret'),
#                      user_agent=conf.get('Bot2', 'user_agent'), password=conf.get('Bot2', 'password'),
#                      username=conf.get('Bot2', 'username'))
#
# names = combinations.comb_ordr_rep__of_len_in_range_str(characs, 4, 5)
#
# print('combinations done', len(names))
#
# fil = open('subreddits4chars.txt', 'a')
#
# for sub in names:
#     try:
#         fil.write(sub+' is NSFW: ' + str(reddit.subreddit(sub).over18) + '\n')
#         print(sub+' is NSFW: ' + str(reddit.subreddit(sub).over18))
#     except Forbidden:
#         pass
#     except NotFound:
#         pass
#     except Exception:
#         pass
#
# print('\ndone')

username = conf.get('Bot2', 'username')
password = conf.get('Bot2', 'password')
client_id = conf.get('Bot2', 'client_id')
client_secret = conf.get('Bot2', 'client_secret')
user_agent = conf.get('Bot2', 'user_agent')
redirect_uri = conf.get('Bot2', 'redirect_uri')
duration = 'temporary'
scope = 'read'

user_pass_dict = {'user': username,
                  'passwd': password,
                  'api_type': 'json', }

headers = {'user-agent': user_agent, }

client = requests.session()
client.headers = headers

r = client.get(f'https://www.reddit.com/api/v1/authorize?client_id={client_id}&response_type=TYPE'
               f'&state=RANDOM_STRING&redirect_uri={redirect_uri}&duration={duration}&scope={scope}.json')

characs = '0123456789abcdefghijklmnopqrstuvwxyz-_'

names = combinations.comb_ordr_rep__of_len_str(characs, 4)

print('combinations done', len(names))

fil = open('subreddits4chars.txt', 'a')

for sub in names:
    res = client.get(f'https://www.reddit.com/r/{sub}/about/.json')
    rep = json.loads(res.text)
    if rep.keys().__contains__('error'):
        continue
    if rep['kind'] == 't5':
        fil.write(sub + ' is NSFW: ' + str(rep['data']['over18']) + '\n')
        print(sub+' is NSFW: ' + str(rep['data']['over18']))
