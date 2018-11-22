import configparser
import praw
from prawcore import NotFound
from prawcore import Forbidden

conf = configparser.ConfigParser()
conf.read('praw.ini')

fil_in = open('subs.txt', 'r')

fil_out_sorted = open('subs_ordr.txt', 'w')

fil_out_public = open('subs_public.txt', 'a')

fil_out_is_nsfw = open('subs_is_nsfw.txt', 'a')

fil_out_nsfw = open('subs_nsfw.txt', 'a')

subs_list = fil_in.readlines()

subs_list_real_name = []

for sub in subs_list:
    subs_list_real_name += [sub[:-1]]

subs_list_sorted = sorted(subs_list_real_name, key=str.lower)

subs_list_sorted_lb = []
for sub in subs_list_sorted:
    subs_list_sorted_lb += [sub + '\n']

print(subs_list_sorted)

fil_out_sorted.writelines(subs_list_sorted_lb)

subs_list_sorted_temp = subs_list_sorted[subs_list_sorted.index('2PartsAnalog')+1:]

subs_list_sorted = subs_list_sorted_temp

reddit = praw.Reddit(client_id=conf.get('Bot2', 'client_id'), client_secret=conf.get('Bot2', 'client_secret'),
                     user_agent=conf.get('Bot2', 'user_agent'), password=conf.get('Bot2', 'password'),
                     username=conf.get('Bot2', 'username'))

print('len:', len(subs_list_sorted))

subs_list_public = []

for sub in subs_list_sorted:
    try:
        is_over_18 = reddit.subreddit(sub).over18
        fil_out_is_nsfw.write(sub+' is NSFW: ' + str(is_over_18) + '\n')
        print(sub + ' is NSFW: ' + str(is_over_18))
        fil_out_public.write(sub + '\n')
        if is_over_18:
            fil_out_nsfw.write(sub + '\n')
    except Forbidden:
        pass
    except NotFound:
        pass
    except Exception:
        pass
