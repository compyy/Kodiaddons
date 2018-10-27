import base64
import datetime
import json
import re

import requests
from bs4 import BeautifulSoup

spk_url = [base64.b64decode('aHR0cHM6Ly93d3cuc2lhc2F0LnBrL2ZvcnVtcy9pbmRleC5waHA/Zm9ydW1zL3NpYXNpLXZpZGVvcy4yMS8='),
           base64.b64decode('aHR0cHM6Ly93d3cuc2lhc2F0LnBrL2ZvcnVtcy9pbmRleC5waHA/Zm9ydW1zL2RhaWx5LXRhbGstc2hvd3MuMjkv'),
           base64.b64decode('aHR0cHM6Ly93d3cuc2lhc2F0LnBrL2ZvcnVtcy9pbmRleC5waHA/Zm9ydW1zL3Nwb3J0cy1jb3JuZXIuMzcv')]
zem_url = [base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vY2F0ZWdvcnkvdmlyYWwtdmlkZW9zLw=='),
           base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vY2F0ZWdvcnkvcGFraXN0YW5pLw==')]

doc_url = base64.b64decode('aHR0cDovL3d3dy5oZGRvY3VtZW50YXJ5LmNvbS9jYXRlZ29yeS9zY2llbmNlLWFuZC10ZWNobm9sb2d5Lw==')

sky_url = base64.b64decode('aHR0cHM6Ly93d3cuc2t5c3BvcnRzLmNvbS93YXRjaC92aWRlby9zcG9ydHMvY3JpY2tldA==')

VIDEO_URL_FMT = 'http://player.ooyala.com/player/all/{video_id}.m3u8'
web_path = '/home/beta/scripts/json/'

p_dm = re.compile("<iframe.*src=.*http.*dailymotion.com.*video[/](.*?)['|/?]")
p_yt = re.compile('<iframe.*?src=\".*?youtube.*?embed\/(.*?)[\"|\?]')
p_pw = re.compile('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"')
p_fb = re.compile('<.*["]http.*facebook[.]com[/]video[.]php[?]v[=](.*?)["]')
p_op = re.compile('.*["]http.*openload[.]co[\/]embed[\/](.*?)[\/]["]')


def spkshows(Fromurl, session):
    spkshows = []
    print(datetime.datetime.now().time())
    print('Downloading sisasatpk Shows...!')
    for link in Fromurl:
        match = []
        for x in range(1, 5):
            newlink = link
            if x is not 1:
                newlink = link + b'page-%d' % x
            data = get_fast(newlink, session)
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
                spkshows.append(empty_check)

    if not spkshows:
        with open(web_path + 'shows.json', 'w', encoding='utf-8') as fout:
            json.dump(spkshows, fout, ensure_ascii=False)
            print('File Writing Successfull..!')

    return


def zemshows(Fromurl, session):
    zemshows = []
    print(datetime.datetime.now().time())
    print('Downloading ZemTV Shows...!')
    for link in Fromurl:
        match = []
        for x in range(1, 4):
            newlink = link
            if x is not 1:
                newlink = link + b'page/%d/' % x
            data = get_fast(newlink, session)
            soup = BeautifulSoup(data, "lxml")
            for div in soup.find_all('div', attrs={'class': 'ui cards'}):
                div_nested = div.descendants
                for d in div_nested:
                    if d.name == 'div' and d.get('class', '') == ['card']:
                        img = div.find_all('img')[0]
                        src = img.get('src')
                        a = div.find_all('a')[1]
                        match.append((src, a.attrs['href'], a.text.strip()))

        for i in match:
            if b'viral' in link:
                empty_check = url_processor(i, "ZEM_Viral", session)
            else:
                empty_check = url_processor(i, "ZEM_Shows", session)
            if empty_check:
                zemshows.append(empty_check)

    if not zemshows:
        with open(web_path + 'zemshows.json', 'w', encoding='utf-8') as fout:
            json.dump(zemshows, fout, ensure_ascii=False)
            print('File Writing Successfull..!')

    return


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


def skyshows(link, session):
    print(datetime.datetime.now().time())
    print('Downloading SkySports Cricket...!')
    match = []
    for x in range(1, 5):
        newlink = link
        if x is not 1:
            newlink = link + b'/more/%d' % x
        data = get_fast(newlink, session)
        soup = BeautifulSoup(data, "lxml")
        for item in soup('div', {'class': 'polaris-tile-grid__item'}):
            thumbnail = item.find('div', 'polaris-tile__media-wrap').img['data-src']
            thumbnail_large = thumbnail.replace('384x216', '768x432')
            heading = item.find('a', 'polaris-tile__heading-link')
            m = re.search('/([\w-]+).jpg', thumbnail)
            if m:
                video_id = m.group(1)
                match.append({'Tag': 'SKYCRIC', 'Title': heading.get_text().strip(), 'icon': thumbnail_large,
                              'link': VIDEO_URL_FMT.format(video_id=video_id)})

    with open(web_path + 'sky.json', 'w', encoding='utf-8') as fout:
        json.dump(match, fout, ensure_ascii=False)

    return


#
#
#

def video_item(video_id, title, thumbnail):
    return {'label': title,
            'thumbnail': thumbnail,
            'path': VIDEO_URL_FMT.format(video_id=video_id),
            'is_playable': True}


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
                imageurl = 'https://img.youtube.com/vi/' + source['Youtube'] + '/hqdefault.jpg'
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
    # sky_session = requests.Session()
    # sky_session.get('https://www.skysports.com/')
    doc_session = requests.Session()
    doc_session.get('http://www.hddocumentary.com/')
    print('Script Starting...! ')
    print(datetime.datetime.now().time())
    spkshows(spk_url, spk_session)
    zemshows(zem_url, zem_session)
    docshows(doc_url, doc_session)
    #skyshows(sky_url, sky_session)
    print('Script Ended')
    print(datetime.datetime.now().time())