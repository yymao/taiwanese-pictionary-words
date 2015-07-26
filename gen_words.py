# coding: utf-8

import re
import json
from itertools import imap
from urllib import urlopen
from bs4 import BeautifulSoup

def iter_chunks(iterable, n):
    return imap(lambda *t: tuple((s.text for s in t)), *(iter(iterable),)*n)

def soup_url(url):
    return BeautifulSoup(urlopen(url).read(), "lxml")

def iter_songs(year_range=range(2000, 2015), n=30):
    for year in year_range:
        soup = soup_url('http://www.hitoradio.com/newweb/chart_2.php?ch_year={}'.format(year))
        for __, song, __, artist in \
                iter_chunks(soup.find('table', {'class':'top100'})('td'), 4):
            l = len(song)
            if l > 1 and l < 10 and not re.search(r'[ -~]', song):
                yield song, artist
            
def iter_stations():
    for sn in range(3606, 3611):
        soup = soup_url('http://www.railway.gov.tw/tw/cp.aspx?sn={}'.format(sn))
        for station, __, __ in \
                iter_chunks(soup.find('caption').findNext('tbody')('td'), 3):
            station = station.strip().rpartition(u'站')[0]
            if station:
                yield station

def iter_phrases():
    soup = soup_url('http://www.twsnap.com/info.php?tid=%E5%B8%B8%E7%94%A8%E6%88%90%E8%AA%9E%E6%9F%A5%E8%A9%A2')
    for t in iter_chunks(soup.find('table', {'class':'table_list'})('td'), 1):
        yield t

def college_name_sub(s):
    s = s.replace(u'國立', u'', 1)
    s = s.replace(u'暨管理專科學校', u'專校', 1)
    s = s.replace(u'管理專科學校', u'專校', 1)
    s = s.replace(u'專科學校', u'專校', 1)
    return s

def iter_colleges():
    soup = soup_url('https://zh.wikipedia.org/zh-tw/%E5%8F%B0%E7%81%A3%E5%A4%A7%E5%B0%88%E9%99%A2%E6%A0%A1%E5%88%97%E8%A1%A8')
    for table in soup.findAll('table', {'class':'wikitable + sortable'})[:-2]:
        for t in iter_chunks(table('td'), 7):
            t = college_name_sub(t[1])
            if len(t) < 10:
                yield t

songs = map(list, iter_songs())
stations = list(iter_stations())
colleges = list(iter_colleges())
phrases = list(iter_phrases())

with open('words.js', 'w') as f:
    f.write('var songs = ')
    json.dump(songs, f)
    f.write(';\n')
    f.write('var stations = ')
    json.dump(stations, f)
    f.write(';\n')
    f.write('var colleges = ')
    json.dump(colleges, f)
    f.write(';\n')
    f.write('var phrases = ')
    json.dump(phrases, f)
    f.write(';\n')

