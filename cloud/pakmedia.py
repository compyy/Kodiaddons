import base64
import datetime
import json
import re

import requests
from bs4 import BeautifulSoup

spk_url = [base64.b64decode('aHR0cHM6Ly93d3cuc2lhc2F0LnBrL2ZvcnVtcy9pbmRleC5waHA/Zm9ydW1zL2RhaWx5LXRhbGstc2hvd3MuMjkv'),
           base64.b64decode('aHR0cHM6Ly93d3cuc2lhc2F0LnBrL2ZvcnVtcy9pbmRleC5waHA/Zm9ydW1zL3NpYXNpLXZpZGVvcy4yMS8='),
           base64.b64decode('aHR0cHM6Ly93d3cuc2lhc2F0LnBrL2ZvcnVtcy9pbmRleC5waHA/Zm9ydW1zL3Nwb3J0cy1jb3JuZXIuMzcv')]
zem_url = [base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vY2F0ZWdvcnkvdmlyYWwtdmlkZW9zLw=='),
           base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vY2F0ZWdvcnkvcGFraXN0YW5pLw==')]

doc_url = base64.b64decode('aHR0cDovL3d3dy5oZGRvY3VtZW50YXJ5LmNvbS9jYXRlZ29yeS9zY2llbmNlLWFuZC10ZWNobm9sb2d5Lw==')

web_path = '/home/beta/scripts/json/'

p_dm = re.compile("<iframe.*src=.*http.*dailymotion.com.*video[/](.*?)['|/?]")
p_yt = re.compile('<iframe.*?src=\".*?youtube.*?embed\/(.*?)[\"|\?]')
p_pw = re.compile('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"')
p_fb = re.compile('<.*["]http.*facebook[.]com[/]video[.]php[?]v[=](.*?)["]')
p_op = re.compile('.*["]http.*openload[.]co[\/]embed[\/](.*?)[\/]["]')


def spkshows(Fromurl, session, shows):
    print(datetime.datetime.now().time())
    print('Downloading sisasatpk Shows...!')
    for link in Fromurl:
        match = []
        data = get_fast(link, session)
        soup = BeautifulSoup(data, "lxml")
        for div in soup.find_all('div', {'class': 'structItem-title'}):
            a = div.find_all('a')[0]
            match.append((a.attrs['data-preview-url'], a.attrs['href'], a.text.strip()))

        link = link + b'page-2'
        data = get_fast(link, session)
        soup = BeautifulSoup(data, "lxml")
        for div in soup.find_all('div', {'class': 'structItem-title'}):
            a = div.find_all('a')[0]
            match.append((a.attrs['data-preview-url'], a.attrs['href'], a.text.strip()))

        for i in match:
            if b'siasi' in link:
                empty_check = url_processor(i, "SP_Viral", session)
            elif b'shows' in link:
                empty_check = url_processor(i, "SP_Shows", session)
            elif b'sports' in link:
                empty_check = url_processor(i, "SP_SC", session)

            if empty_check:
                shows.append(empty_check)

    with open(web_path + 'shows.json', 'w', encoding='utf-8') as fout:
        json.dump(shows, fout, ensure_ascii=False)
        print('File Writing Successfull..!')

    return


def zemshows(Fromurl, session):
    print(datetime.datetime.now().time())
    print('Downloading Zem Shows...!')
    shows = []
    for link in Fromurl:
        orig_link = link
        linkfull = get_fast(link, session)
        pageNumber = 1
        catid = ''

        if not b'loopHandler' in link:
            catid = re.findall("currentcat = (.*?);", linkfull)[0]
            link = 'http://www.zemtv.com/wp-content/themes/zemresponsive/loopHandler.php?pageNumber=%s&catNumber=%s' % (
                str(pageNumber), catid)
            linkfull = get_fast(link, session)

        match = re.findall('<div class=\"(?:teal)?.?card\">.*?<img src=\"(.*?)\".*?<a href=\"(.*?)\".*?>(.*?)<',
                           linkfull,
                           re.UNICODE | re.DOTALL)

        pageNumber = re.findall("pageNumber=(.*?)&", link)[0]
        catid = re.findall("catNumber=(.*)", link)[0]
        pageNumber = int(pageNumber) + 1
        link = 'http://www.zemtv.com/wp-content/themes/zemresponsive/loopHandler.php?pageNumber=%s&catNumber=%s' % (
            str(pageNumber), catid)
        linkfull = get_fast(link, session)
        match.extend(
            re.findall('<div class=\"(?:teal)?.?card\">.*?<img src=\"(.*?)\".*?<a href=\"(.*?)\".*?>(.*?)<', linkfull,
                       re.UNICODE | re.DOTALL))

        pageNumber = re.findall("pageNumber=(.*?)&", link)[0]
        catid = re.findall("catNumber=(.*)", link)[0]
        pageNumber = int(pageNumber) + 1
        link = 'http://www.zemtv.com/wp-content/themes/zemresponsive/loopHandler.php?pageNumber=%s&catNumber=%s' % (
            str(pageNumber), catid)
        linkfull = get_fast(link, session)
        match.extend(
            re.findall('<div class=\"(?:teal)?.?card\">.*?<img src=\"(.*?)\".*?<a href=\"(.*?)\".*?>(.*?)<', linkfull,
                       re.UNICODE | re.DOTALL))

        for i in match:
            if b'viral' in orig_link:
                empty_check = url_processor(i, "ZEM_Viral", session)
            else:
                empty_check = url_processor(i, "ZEM_Shows", session)

            if empty_check:
                shows.append(empty_check)

    return shows


def docshows(link, session):
    print(datetime.datetime.now().time())
    print('Downloading Doc Shows...!')
    docshows = []
    match = []
    data = get_fast(link, session)
    soup = BeautifulSoup(data, "lxml")
    for i in soup.find_all('article'):
        a = i.find_all(class_='post-image post-image-left')[0]
        icon = ((a.find('div', {'class': 'featured-thumbnail'})).find('img').attrs['src'])
        match.append((icon, a.attrs['href'], a.attrs['title']))

    for i in match:
        docshows.append(url_processor(i, "DOCHD", session))

    with open(web_path + 'docshows.json', 'w', encoding='utf-8') as fout:
        json.dump(docshows, fout, ensure_ascii=False)

    return


#
def url_processor(cname, tag, session):
    shows = []
    if 'forums' in cname[1]:
        tname = cname[2]
        url = cname[1]
        imageurl = str(cname[0])
        if not url.startswith('http'):
            url = 'http://www.siasat.pk' + url
        if not imageurl.startswith('http'):
            imageurl = 'http://www.siasat.pk' + imageurl
    else:
        tname = cname[2]
        url = cname[1]
        imageurl = cname[0]

    link = get_fast(url, session)
    source = {}
    did = re.search(p_dm, link)
    if did:
        source['DailyMotion'] = did.groups(0)[0]

    yid = re.search(p_yt, link)
    if yid:
        source['Youtube'] = yid.groups(0)[0]

    fid = re.search(p_fb, link)
    if fid:
        source['Facebook'] = fid.groups(0)[0]

    pid = re.search(p_pw, link)
    if pid:
        source['Playwire'] = pid.groups(0)[0]

    oid = re.search(p_op, link)
    if oid:
        source['Openload'] = oid.groups(1)[0]

    if len(source) > 0:
        if 'forums' in imageurl:
            if 'Youtube' in source:
                imageurl = 'https://img.youtube.com/vi/' + source['Youtube'] + '/maxresdefault.jpg'
            elif 'DailyMotion' in source:
                imageurl = 'https://www.dailymotion.com/thumbnail/video/' + source['DailyMotion']
        shows = ({'Tag': tag, 'Title': tname, 'icon': imageurl, 'link': source})

    return shows


#

def get_fast(url, session):
    data = session.get(url)
    return data.text


if __name__ == "__main__":
    zem_session = requests.Session()
    zem_session.get('http://www.zemtv.com/')
    spk_session = requests.Session()
    spk_session.get('https://www.siasat.pk/forum/home.php')
    print('Script Starting...! ')
    print(datetime.datetime.now().time())
    shows = zemshows(zem_url, zem_session)
    # shows=[]
    spkshows(spk_url, spk_session, shows)
    doc_session = requests.Session()
    doc_session.get('http://www.hddocumentary.com/')
    docshows(doc_url, doc_session)
    print('Script Ended')
    print(datetime.datetime.now().time())
