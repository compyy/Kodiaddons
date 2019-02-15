import base64
import datetime
import json
import re
import sys

import requests
import xbmc
import xbmcaddon
import xbmcgui

#
sys.path.append(xbmcaddon.Addon(id='script.module.beautifulsoup4').getAddonInfo("path") + '/lib')
from bs4 import BeautifulSoup

#
addon_id = 'plugin.video.PakMedia'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonPath = selfAddon.getAddonInfo("path")
json_path = addonPath + '/resources/json/'

###
spk_url = [base64.b64decode('aHR0cHM6Ly93d3cuc2lhc2F0LnBrL2ZvcnVtcy9mb3J1bXMvc2lhc2ktdmlkZW9zLjIxLw=='),
           base64.b64decode('aHR0cHM6Ly93d3cuc2lhc2F0LnBrL2ZvcnVtcy9mb3J1bXMvZGFpbHktdGFsay1zaG93cy4yOS8='),
           base64.b64decode('aHR0cHM6Ly93d3cuc2lhc2F0LnBrL2ZvcnVtcy9mb3J1bXMvc3BvcnRzLWNvcm5lci4zNy8=')]

zem_url = [base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vY2F0ZWdvcnkvdmlyYWwtdmlkZW9zLw=='),
           base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vY2F0ZWdvcnkvcGFraXN0YW5pLw==')]

doc_url = base64.b64decode('aHR0cDovL3d3dy5oZGRvY3VtZW50YXJ5LmNvbS9jYXRlZ29yeS9zY2llbmNlLWFuZC10ZWNobm9sb2d5Lw==')

sky_url = base64.b64decode('aHR0cHM6Ly93d3cuc2t5c3BvcnRzLmNvbS93YXRjaC92aWRlby9zcG9ydHMvY3JpY2tldA==')

p_dm = re.compile("<iframe.*src=.*http.*dailymotion.com.*video[/](.*?)['|/?]")
p_yt = re.compile('<iframe.*?src=\".*?youtube.*?embed\/(.*?)[\"|\?]')
p_pw = re.compile('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"')
p_fb = re.compile('<.*["]http.*facebook[.]com[/]video[.]php[?]v[=](.*?)["]')
p_op = re.compile('.*["]http.*openload[.]co[\/]embed[\/](.*?)[\/]["]')


###
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
            soup = BeautifulSoup(data, 'html.parser')
            for div in soup.find_all('div', {'class': 'structItem-title'}):
                if "contentRow" in div["class"][0]:
                    continue
                a = div.find_all('a')[0]
                match.append((a.attrs['data-preview-url'].encode('utf-8'), a.attrs['href'].encode('utf-8'),
                              a.text.strip().encode('utf-8')))

        for i in match:
            if b'siasi' in link:
                empty_check = url_processor(i, "SP_Viral", session)
            elif b'shows' in link:
                empty_check = url_processor(i, "SP_Shows", session)
            elif b'sports' in link:
                empty_check = url_processor(i, "SP_SC", session)

            if empty_check:
                spkshows.append(empty_check)

    if spkshows:
        with open(json_path + 'spkshows.json', 'w') as fout:
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
            soup = BeautifulSoup(data, 'html.parser')
            for div in soup.find_all('div', attrs={'class': 'ui cards'}):
                div_nested = div.descendants
                for d in div_nested:
                    if d.name == 'div' and d.get('class', '') == ['card']:
                        img = div.find_all('img')[0]
                        src = img.get('src')
                        a = div.find_all('a')[1]
                        match.append((src, a.attrs['href'].encode('utf-8'), a.text.strip().encode('utf-8')))

        for i in match:
            if b'viral' in link:
                empty_check = url_processor(i, "ZEM_Viral", session)
            else:
                empty_check = url_processor(i, "ZEM_Shows", session)
            if empty_check:
                zemshows.append(empty_check)

    if zemshows:
        with open(json_path + 'zemshows.json', 'w') as fout:
            json.dump(zemshows, fout, ensure_ascii=False)
            print('File Writing Successfull..!')

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

    if "SP" in tag:
        data = get_fast(url, session)
        soup = BeautifulSoup(data, 'html.parser')
        div = soup.find('div', {'class': 'bbWrapper'})
        link = str(div)

    else:
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


#
def shows_update():
    zem_session = requests.Session()
    zem_session.get('http://www.zemtv.com/')
    spk_session = requests.Session()
    spk_session.get('https://www.siasat.pk/forum/home.php')
    spkshows(spk_url, spk_session)
    zemshows(zem_url, zem_session)


#
###
xbmc.log('Shows Update Start ' + str(datetime.datetime.now().time()), level=xbmc.LOGNOTICE)
dialog = xbmcgui.Dialog()
xbmc.log('Shows Update Start ' + str(datetime.datetime.now().time()), level=xbmc.LOGNOTICE)
dialog.notification('Shows Update', 'Shows Update Started ' + str(datetime.datetime.now().time()),
                    xbmcgui.NOTIFICATION_INFO, 5000)
# shows_update()
dialog.notification('Shows Update', 'Shows Update Ended ' + str(datetime.datetime.now().time()),
                    xbmcgui.NOTIFICATION_INFO, 5000)
