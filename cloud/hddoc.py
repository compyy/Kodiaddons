import base64
import datetime
import json
import re
import time

import requests
from bs4 import BeautifulSoup

doc_url = base64.b64decode('aHR0cDovL3d3dy5oZGRvY3VtZW50YXJ5LmNvbS9jYXRlZ29yeS9zY2llbmNlLWFuZC10ZWNobm9sb2d5Lw==')

web_path = '/home/beta/scripts/json/'

p_op = re.compile('.*["]http.*openload[.]co[\/]embed[\/](.*?)[\/]["]')


def docshows(link):
    docshows = []
    match = []
    data = get_fast(link)
    soup = BeautifulSoup(data, "lxml")
    for i in soup.find_all('article'):
        a = i.find_all(class_='post-image post-image-left')[0]
        icon = ((a.find('div', {'class': 'featured-thumbnail'})).find('img').attrs['src'])
        match.append((icon, a.attrs['href'], a.attrs['title']))

    for i in match:
        docshows.append(url_processor(i, "DOCHD"))

    for i in range(2, 114):
        time.sleep(3)
        nextlink = str(link)
        nextlink = nextlink[2:-1] + 'page/' + str(i) + '/'
        print(nextlink)
        data = get_fast(nextlink)
        soup = BeautifulSoup(data, "lxml")
        for i in soup.find_all('article'):
            a = i.find_all(class_='post-image post-image-left')[0]
            icon = ((a.find('div', {'class': 'featured-thumbnail'})).find('img').attrs['src'])
            match.append((icon, a.attrs['href'], a.attrs['title']))

        for i in match:
            docshows.append(url_processor(i, "DOCHD"))

        print('Done')

    with open(web_path + 'docshows.json', 'w', encoding='utf-8') as fout:
        json.dump(docshows, fout, ensure_ascii=False)

    return


#
def url_processor(cname, tag):
    shows = []
    if 'forum' in cname[1]:
        tname = cname[2]
        url = cname[1]
        imageurl = str(cname[0]).replace('&amp;', '&')
        if not url.startswith('http'):
            url = 'http://www.siasat.pk' + url
        if not imageurl.startswith('http'):
            imageurl = 'http://www.siasat.pk' + url
    else:
        tname = cname[2]
        url = cname[1]
        imageurl = cname[0]

    link = get_fast(url)
    source = {}
    oid = re.search(p_op, link)
    if oid:
        source['Openload'] = oid.groups(1)[0]

    if len(source) > 0:
        shows = ({'Tag': tag, 'Title': tname, 'icon': imageurl, 'link': source})

    return shows


#

def get_fast(url):
    data = requests.get(url)
    return data.text


if __name__ == "__main__":
    print(datetime.datetime.now().time())
    docshows(doc_url)
    print(datetime.datetime.now().time())
