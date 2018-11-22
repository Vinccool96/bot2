import configparser

import csv
import json

import requests
import datetime

time_started = datetime.datetime.utcnow()
print('time started: ' + str(time_started))

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

time_started_to_get_list_of_subs = datetime.datetime.utcnow()
print('time to get list of subs: ' + str(time_started_to_get_list_of_subs))

fil_subredds = open('subredds.txt', 'w', newline='\n')

list_infos = []

with open('subreddits_basic.csv', newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',', )
    for row in csvreader:
        list_infos += [row]

list_subs = []

for infos in list_infos:
    list_subs += [infos[3]]

list_subs_sorted = sorted(list_subs, key=str.upper)

for sub_sorted in list_subs_sorted:
    fil_subredds.write(sub_sorted + '\n')

time_subs_sorted = datetime.datetime.utcnow()
print('time subs are sorted: ' + str(time_subs_sorted))

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

time_started_to_get_infos = datetime.datetime.utcnow()
print('time started to get infos: ' + str(time_started_to_get_infos))

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

time_infos_received = datetime.datetime.utcnow()
print('time info is received: ' + str(time_infos_received))

zips = [(fil_subredds_at_large, list_subredds_at_large), (fil_subredds_public, list_subredds_public),
        (fil_subredds_is_it_nsfw, list_subredds_is_it_nsfw), (fil_subredds_sfw, list_subredds_sfw),
        (fil_subredds_nsfw, list_subredds_nsfw), (fil_subredds_gold_restricted, list_subredds_gold_restricted)]

time_started_writing_infos = datetime.datetime.utcnow()
print('time started writing infos: ' + str(time_started_writing_infos))

for z in zips:
    f, l_subs = z[0], z[1]
    for s in l_subs:
        f.write(s + '\n')

time_ended = datetime.datetime.utcnow()
print('time ended: ' + str(time_ended))

with open('timestamps.txt', 'w') as fil_timestamps:
    fil_timestamps.write('time started: ' + str(time_started) + '\n')
    fil_timestamps.write('time to get list of subs: ' + str(time_started_to_get_list_of_subs) + '\n')
    fil_timestamps.write('time subs are sorted: ' + str(time_subs_sorted) + '\n')
    fil_timestamps.write('time started to get infos: ' + str(time_started_to_get_infos) + '\n')
    fil_timestamps.write('time info is received: ' + str(time_infos_received) + '\n')
    fil_timestamps.write('time started writing infos: ' + str(time_started_writing_infos) + '\n')
    fil_timestamps.write('time ended: ' + str(time_ended) + '\n')
