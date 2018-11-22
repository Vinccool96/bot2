import configparser
import csv
import json

import requests

conf = configparser.ConfigParser()
conf.read('praw.ini')

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

fil_subredds = open('subredds.txt', 'w', newline='\n')

list_infos = []

with open('subreddits_basic.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', )
    for row in spamreader:
        list_infos += [row]

list_subs = []

for infos in list_infos:
    list_subs += [infos[3]]

list_subs_sorted = sorted(list_subs, key=str.upper)

for sub_sorted in list_subs_sorted:
    fil_subredds.write(sub_sorted + '\n')

fil_subredds_at_large = open('subredds_at_large.txt', 'w', newline='\n')

fil_subredds_public = open('subredds_public.txt', 'w', newline='\n')

fil_subredds_is_it_nsfw = open('subredds_is_it_nsfw.txt', 'w', newline='\n')

fil_subredds_sfw = open('subredds_sfw.txt', 'w', newline='\n')

fil_subredds_nsfw = open('subredds_nsfw.txt', 'w', newline='\n')

fil_subredds_gold_restricted = open('subredds_gold_restricted.txt', 'w', newline='\n')

list_subredds_at_large = []

list_subredds_public = []

list_subredds_is_it_nsfw = []

list_subredds_sfw = []

list_subredds_nsfw = []

list_subredds_gold_restricted = []

for sub in list_subs_sorted:
    res = client.get(f'https://www.reddit.com/r/{sub}/about/.json')
    rep = json.loads(res.text)
    if rep.keys().__contains__('error'):
        continue
    elif rep['kind'] == 't5':
        list_subredds_at_large.append(sub)
        if rep['data']['subreddit_type'] == 'public':
            list_subredds_public.append(sub)
            isOver18 = rep['data']['over18']
            list_subredds_is_it_nsfw.append(sub + ' is NSFW: ' + str(isOver18))
            print(sub + ' is NSFW: ' + str(isOver18))
            (list_subredds_nsfw if isOver18 else list_subredds_sfw).append(sub)
        if rep['data']['subreddit_type'] == 'gold_restricted':
            list_subredds_gold_restricted.append(sub)

zips = [(fil_subredds_at_large, list_subredds_at_large), (fil_subredds_public, list_subredds_public),
        (fil_subredds_is_it_nsfw, list_subredds_is_it_nsfw), (fil_subredds_sfw, list_subredds_sfw),
        (fil_subredds_nsfw, list_subredds_nsfw), (fil_subredds_gold_restricted, list_subredds_gold_restricted)]

for z in zips:
    f, l_subs = z[0], z[1]
    for s in l_subs:
        f.write(s + '\n')
