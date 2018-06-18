#!/usr/bin/env python
# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from urlparse import urljoin, urlparse
import requests
import grab
import pandas as pd
from tqdm import tqdm
from IPython.display import HTML, display
import time
from bs4 import BeautifulSoup
from types import *
import json

pd.options.display.max_colwidth = 300

page_link = 'https://m.habr.com/post/'
start = 2000
finish = 3000
date = {}
user = {}
for i in range(start, finish):
    path = str(i) + 'comments.csv'
    print path
    x = pd.read_csv(path, sep='\t')
    for j in range(len(x)):
        user_id = str(x['id'][j])
        score = int(x['score'][j])
        time = str(x['time'][j])[:8].replace('.', '-')
        t = str(x['time'][j])
        all_time = t[6:8] + '-' + t[3:5] + '-' + t[0:2] + '-' + t[12:].replace(':', '-')
        #print all_time
        user_name = str(x['username'][j])
        if date.get(time, False):
            date[time].append([user_id, score, all_time])
        else:
            date[time] = [[user_id, score, all_time]]
        if user.get(user_name, False):
            user[user_name].append([user_id, score, all_time])
        else:
            user[user_name] = [[user_id, score, all_time]]
with open("date.json", 'w') as f_out:
    json.dump(date, f_out)
with open("date.json", 'w') as f_out:
    f_out.write(json.dumps(date))

with open("user.json", 'w') as f_out:
    json.dump(user, f_out)
with open("user.json", 'w') as f_out:
    f_out.write(json.dumps(user))

#with open("date.json") as f_in:
#    date = json.load(f_in)
#with open("date.json") as f_in:
#    date = json.loads(f_in.read())
