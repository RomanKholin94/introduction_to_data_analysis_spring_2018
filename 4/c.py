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

pd.options.display.max_colwidth = 300

def get_page(url):
    page = requests.get(url)
    while page == '':
        try:
            page = requests.get(url)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    if page.ok:
        html = page.content
        soup = BeautifulSoup(html,'html.parser')
        title = soup.find('h3', attrs = {'class':'title'}).text[7:-5]
        author = soup.find('a', attrs = {'class':'author'})
        if not (type(author) is NoneType):
            author = author.text
        else:
            print url
            author = ''
        time = soup.find('span', attrs = {'class':'time'}).text[:-8]
        return True, [title, author, time]
    return False, []

def get_comments(url, i):
    results = []

    page = ''
    while page == '':
        try:
            page = requests.get(url)
            break
        except:
            print("Connection refused by the server..")
            print("Let me sleep for 5 seconds")
            print("ZZzzzz...")
            time.sleep(5)
            print("Was a nice sleep, now let me continue...")
            continue
    bs = BeautifulSoup(page.content, 'lxml')
    for x in bs.find_all('div', 'comment_item_inner'):
        results.append({
            'score': int(x.find('span', 'score').text.replace(u'\u2013', '-')),
            'username': x.find('a', 'username').text,
            'time': x.find('a', 'time').text,
            'id': i + urljoin(url, x.find('a', 'time').get('href'))[39:]
        })
    return results
page_link = 'https://m.habr.com/post/'
start = 287900
finish = 300000
posts = []
comments = []
#with open("date.json") as f_in:
#    date = json.load(f_in)
#with open("date.json") as f_in:
#    date = json.loads(f_in.read())
for i in range(start, finish):
    if i % 100 == 99:
        print i, len(posts), len(comments)
        posts = pd.DataFrame(posts)
        comments = pd.DataFrame(comments)
        posts.to_csv(str(i / 100) + "posts.csv", sep='\t', encoding='utf-8')
        comments.to_csv(str(i / 100) + "comments.csv", sep='\t', encoding='utf-8')
        posts = []
        comments = []
    f, x = get_page(page_link + str(i))
    if f:
        posts.append(x)
        comments.extend(get_comments(page_link + str(i) + '/comments', str(i)))
posts = pd.DataFrame(posts)
comments = pd.DataFrame(comments)

posts.to_csv("posts.csv", sep='\t', encoding='utf-8')

comments.to_csv("comments.csv", sep='\t', encoding='utf-8')
