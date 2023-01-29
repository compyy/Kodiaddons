import base64
import datetime
import json
import re
import sys
import time

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
spk_url = [base64.b64decode('aHR0cHM6Ly93d3cuc2lhc2F0LnBrL2ZvcnVtcy9zaWFzaS12aWRlb3MuMjEv'),
           base64.b64decode('aHR0cHM6Ly93d3cuc2lhc2F0LnBrL2ZvcnVtcy9kYWlseS10YWxrLXNob3dzLjI5Lw=='),
           base64.b64decode('aHR0cHM6Ly93d3cuc2lhc2F0LnBrL2ZvcnVtcy9zcG9ydHMtY29ybmVyLjM3Lw==')]

p_dm = re.compile("<iframe.*src=.*http.*dailymotion.com.*video[/](.*?)[\"|\'|/?]")
p_yt = re.compile('<iframe.*?src=\".*?youtube.*?embed\/(.*?)[\"|\?]')
p_pw = re.compile('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"')
p_fb = re.compile('<.*["]http.*facebook[.]com[/]video[.]php[?]v[=](.*?)["]')
p_op = re.compile('.*["]http.*openload[.]co[\/]embed[\/](.*?)[\/]["]')


###
def spkshows(Fromurl, session):
    spkshows = []
    print('Downloading sisasatpk Shows...!')
    for link in Fromurl:
        match = []
        for x in range(1, 5):
            newlink = link
            if x != 1:
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
        show_end_time = datetime.datetime.now()
        show_end_time = show_end_time.strftime("%d/%m/%Y, %H:%M:%S")
        show_end_time_SP_Viral = {"Tag": "SP_Viral", "Title": show_end_time, "icon": "DefaultYear.png",
                                  "link": {"Youtube": ""}}
        show_end_time_SP_Shows = {"Tag": "SP_Shows", "Title": show_end_time, "icon": "DefaultYear.png",
                                  "link": {"Youtube": ""}}
        show_end_time_SP_SC = {"Tag": "SP_SC", "Title": show_end_time, "icon": "DefaultYear.png",
                               "link": {"Youtube": ""}}
        spkshows.insert(0, show_end_time_SP_SC)
        spkshows.insert(0, show_end_time_SP_Shows)
        spkshows.insert(0, show_end_time_SP_Viral)

        with open(json_path + 'spkshows.json', 'w', encoding='utf-8') as fout:
            json.dump(spkshows, fout, ensure_ascii=False)
            print('File Writing Successfull..!')
    return


#
def url_processor(cname, tag, session):
    shows = []
    if b'forums' in cname[1]:
        tname = cname[2].decode('utf-8')
        url = cname[1]
        imageurl = str(cname[0])
        if not url.startswith(b'http'):
            url = b'http://www.siasat.pk' + url
        if not imageurl.startswith('http'):
            imageurl = 'http://www.siasat.pk' + imageurl
    else:
        tname = cname[2].decode('utf-8')
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
    spk_session = requests.Session()
    spk_session.get('https://www.siasat.pk/forum/home.php')
    spkshows(spk_url, spk_session)


#
###
with open(addonPath + '/runtime', 'w') as fout:
    fout.write(str(time.time()))

xbmc.log('Shows Update Start ' + str(datetime.datetime.now().time()), level=xbmc.LOGINFO)
dialog = xbmcgui.Dialog()
xbmc.log('Shows Update Start ' + str(datetime.datetime.now().time()), level=xbmc.LOGINFO)
dialog.notification('Shows Update', 'Shows Update Started ' + str(datetime.datetime.now().time()),
                    xbmcgui.NOTIFICATION_INFO, 5000)
shows_update()
dialog.notification('Shows Update', 'Shows Update Ended ' + str(datetime.datetime.now().time()),
                    xbmcgui.NOTIFICATION_INFO, 5000)