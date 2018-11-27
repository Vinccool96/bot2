import configparser

import csv
import json

import requests
import datetime

time_started = datetime.datetime.utcnow()
with open('timestamps.txt', 'a') as fil_timestamps:
    fil_timestamps.write('time started: ' + str(time_started)+'\n')
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
with open('timestamps.txt', 'a') as fil_timestamps:
    fil_timestamps.write('time to get list of subs: ' + str(time_started_to_get_list_of_subs)+'\n')
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

list_infos = None
list_subs_sorted = sorted(list_subs, key=str.upper)
list_subs = None

for sub_sorted in list_subs_sorted:
    fil_subredds.write(sub_sorted + ('\n' if sub_sorted != list_subs_sorted[-1] else ''))

fil_subredds.close()

time_subs_sorted = datetime.datetime.utcnow()
with open('timestamps.txt', 'a') as fil_timestamps:
    fil_timestamps.write('time subs are sorted: ' + str(time_subs_sorted)+'\n')
print('time subs are sorted: ' + str(time_subs_sorted))

time_started_to_get_infos = datetime.datetime.utcnow()
with open('timestamps.txt', 'a') as fil_timestamps:
    fil_timestamps.write('time started to get infos: ' + str(time_started_to_get_infos)+'\n')
print('time started to get infos: ' + str(time_started_to_get_infos))

for sub in list_subs_sorted[list_subs_sorted.index('DadMemesandMore')+1:]:
    res = client.get(f'https://www.reddit.com/r/{sub}/about/.json')
    rep = json.loads(res.text)
    if rep.keys().__contains__('error') or rep.keys().__contains__('reason'):
        continue
    elif rep['kind'] == 't5':
        with open('subredds_at_large.txt', 'a', newline='\n') as fil_subredds_at_large:
            fil_subredds_at_large.write(sub+'\n')
        if rep['data']['subreddit_type'] == 'public':
            with open('subredds_public.txt', 'a', newline='\n') as fil_subredds_public:
                fil_subredds_public.write(sub+'\n')
            isOver18 = rep['data']['over18']
            with open('subredds_is_it_nsfw.txt', 'a', newline='\n') as fil_subredds_is_it_nsfw:
                fil_subredds_is_it_nsfw.write(sub + ' is NSFW: ' + str(isOver18)+'\n')
            print(sub + ' is NSFW: ' + str(isOver18))
            with open(f"subredds_{'nsfw' if isOver18 else 'sfw'}.txt", 'a', newline='\n') as fil_subredds_xsfw:
                fil_subredds_xsfw.write(sub+'\n')
        elif rep['data']['subreddit_type'] == 'gold_restricted':
            with open('subredds_gold_restricted.txt', 'a', newline='\n') as fil_subredds_gold_restricted:
                fil_subredds_gold_restricted.write(sub+'\n')

time_ended = datetime.datetime.utcnow()
with open('timestamps.txt', 'a') as fil_timestamps:
    fil_timestamps.write('time ended: ' + str(time_ended) + '\n')
print('time ended: ' + str(time_ended))
