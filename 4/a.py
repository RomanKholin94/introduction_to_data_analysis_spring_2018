#!/usr/bin/env python
# -*- coding: utf-8 -*-



import socket

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
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
import unicodedata
import json
from unidecode import unidecode
import sys, locale
import chardet

#with open("user.json") as f_in:
#    User = json.load(f_in)
#with open("user.json") as f_in:
#    User = json.loads(f_in.read())
#with open("date.json") as f_in:
#    Date = json.load(f_in)
#with open("date.json") as f_in:
#    Date = json.loads(f_in.read())
print "ok"

class HttpProcessor(BaseHTTPRequestHandler):
    pd.options.display.max_colwidth = 300

    def right_date(self, s):
        s = s.split()
        x = ''
        if s[1][:3] == u'янв':
            x = '01'
        elif s[1][:3] == u'фев':
            x = '02'
        elif s[1][:3] == u'мар':
            x = '03'
        elif s[1][:3] == u'апр':
            x = '04'
        elif s[1][:2] == u'ма':
            x = '05'
        elif s[1][:3] == u'июн':
            x = '06'
        elif s[1][:3] == u'июл':
            x = '07'
        elif s[1][:3] == u'авг':
            x = '08'
        elif s[1][:3] == u'сен':
            x = '09'
        elif s[1][:3] == u'окт':
            x = '10'
        elif s[1][:3] == u'ноя':
            x = '11'
        elif s[1][:3] == u'дек':
            x = '12'
        while len(s[2]) < 2:
            s[2] = '0' + s[2]
        while len(s[0]) < 2:
            s[0] = '0' + s[0]
        return s[2] + '-' + x + '-' + s[0]

    def get_page(self, url):
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

    def get_comments(self, url, i):
        results = []
        print url
 
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
                'score': -int(x.find('span', 'score').text.replace(u'\u2013', '-')),
                'username': x.find('a', 'username').text,
                'time': x.find('a', 'time').text[6:8] + '-' + x.find('a', 'time').text[3:5] + '-' + x.find('a', 'time').text[0:2] + '-' + x.find('a', 'time').text[11:13] + '-' + x.find('a', 'time').text[14:16],
                'id': i + urljoin(url, x.find('a', 'time').get('href'))[39:]
            })
        return results
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()

        page_link = 'https://m.habr.com/post/'

        d = self.path[1:]

        print "====================Test cases=================="
            
        print d

        if d[:len("post_top_comments")] == "post_top_comments":
            post_id = d.split('&')[0].split('=')[1]
            n = int(d.split('&')[1].split('=')[1])
            x = self.get_comments(page_link + post_id + '/comments', post_id);
            #print x
            x = pd.DataFrame(x).sort_values(['score', 'time'], ascending=True)
            print x
            x = {"comments" : x['id'].tolist()[0:n]}
            self.wfile.write(str(x).replace("\'", "\""))
        elif d[:len("post_title")] == "post_title":
            d = int(d[-6:])
            f, x = self.get_page(page_link + str(d))
            s = x[0].encode("utf-8")
            s = "{\"title\" : \"" + s + "\"}"
            self.wfile.write(s)
        elif d[:len("post_author")] == "post_author":
            d = int(d[-6:])
            f, x = self.get_page(page_link + str(d))
            self.wfile.write("{\"author\" : \"" + x[1] + "\"}")
        elif d[:len("post_date")] == "post_date":
            d = int(d[-6:])
            f, x = self.get_page(page_link + str(d))

            self.wfile.write(str({"date" : str(self.right_date(x[2]))}).replace("\'", "\""))
        elif d[:len("date_top_comments")] == "date_top_comments":
            date = d.split('&')[0].split('=')[1]
            print date
            date = date[8:10] + '-' + date[5:7] + '-' + date[2:4]
            print date
            n = int(d.split('&')[1].split('=')[1])
            with open("date.json") as f_in:
                Date = json.load(f_in)
            with open("date.json") as f_in:
                Date = json.loads(f_in.read())
            ans = {"comments" : []}
            a = sorted(Date[date], key=lambda x: (-int(x[1]), x[2]))
            for i in range(min(n, len(a))):
                ans["comments"].append(str(a[i][0]))
                print str(a[i])
            self.wfile.write(str(ans).replace("\'", "\""))
        elif d[:len("user_top_comments")] == "user_top_comments":
            user_id = d.split('&')[0].split('=')[1]
            n = int(d.split('&')[1].split('=')[1])
            with open("user.json") as f_in:
                User = json.load(f_in)
            with open("user.json") as f_in:
                User = json.loads(f_in.read())
            a = sorted(User[user_id], key=lambda x: (-int(x[1]), x[2]))
            ans = {"comments" : []}
            for i in range(n):
                ans["comments"].append(str(a[i][0]))
                print str(a[i])
            self.wfile.write(str(ans).replace("\'", "\""))
        else:
            self.wfile.write("ok")
        print "\n"

serv = HTTPServer(("localhost", 5000), HttpProcessor)
serv.serve_forever()
