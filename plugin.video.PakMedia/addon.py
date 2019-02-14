import base64
import datetime
import json
import os
import re
import sys
import traceback
import urllib

import requests
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

#
sys.path.append(xbmcaddon.Addon(id='script.module.beautifulsoup4').getAddonInfo("path") + '/lib')
from bs4 import BeautifulSoup
#
# End of Imports
#
# Setting up basic Variables for XBMC ####
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')

addon_id = 'plugin.video.PakMedia'
selfAddon = xbmcaddon.Addon(id=addon_id)
profile_path = xbmc.translatePath(selfAddon.getAddonInfo('profile'))
addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonversion = xbmcaddon.Addon().getAddonInfo("version")
sys.path.append(os.path.join(addonPath, 'resources', 'lib'))

spicon = addonPath + '/resources/icon/siasatpk.png'
docicon = addonPath + '/resources/icon/docu.png'
skyicon = addonPath + '/resources/icon/skysports.png'
zmicon = addonPath + '/resources/icon/zem.jpg'
smicon = addonPath + '/resources/icon/smartcric.png'
docshowjson = addonPath + '/resources/lib/'
json_path = addonPath + '/resources/json/'

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

# Initializing the settings ###
if not selfAddon.getSetting("dummy") == "true":
    selfAddon.setSetting("dummy", "true")


# Define settting function ###
def show_settings():
    selfAddon.openSettings()


# End of Addon Class info and setting ####

##### Define Functions #####
def add_types():
    add_directory('Daily Talk Shows', 'SP_Shows', 2, spicon)
    add_directory('Daily Vidoes', 'SP_Viral', 2, spicon)
    add_directory('Sports Corner', 'SP_SC', 2, spicon)
    add_directory('ZemTV Shows', 'ZEM_Shows', 2, zmicon)
    add_directory('Zemtv Videos', 'ZEM_Viral', 2, zmicon)
    add_directory('Refresh Shows', 'refresh_shows', 2, '')
    add_directory('SmartCric', 'SMARTCRIC', 2, smicon)
    add_directory('SkySports Cricket', 'SKYCRIC', 2, skyicon)
    add_directory('Documentry HD', 'DOCHD', 2, docicon)
    add_directory('Documentry HD April-2018', 'DOCHDOLD', 2, docicon)
    add_directory('Settings', 'Settings', 99, 'OverlayZIP.png', isItFolder=False)

    return


def add_directory(name, url, mode, iconimage, showContext=False, isItFolder=True, linkType=None):
    if mode == 3:
        u = sys.argv[0] + "?url=" + urllib.quote_plus(url.values()[0]) + "&mode=" + str(
            mode) + "&name=" + urllib.quote_plus(name) + "&provider=" + url.keys()[0]
    else:
        u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)

    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    if showContext:
        cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "DailyMotion")
        cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "Youtube")
        cmd3 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "Facebook")
        cmd4 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "Playwire")
        cmd5 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "Checksrc")
        liz.addContextMenuItems(
            [('Play DailyMotion video', cmd1), ('Play Youtube video', cmd2), ('Play Facebook video', cmd3),
             ('Play Playwire video', cmd4), ('Check Available Sources', cmd5)],
            replaceItems=True)
    if linkType:
        u = "XBMC.RunPlugin(%s&linkType=%s)" % (u, linkType)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isItFolder)
    return ok


def add_enteries(url_type=None):
    if url_type:
        if 'DOCHD' in url_type:
            url = urllib.urlopen("http://192.168.0.160/docshows.json")
            shows_json = json.loads(url.read().decode("utf-8"))
            add_shows(url_type, shows_json)

        if 'DOCHDOLD' in url_type:
            with open(docshowjson + 'docshowsold.json') as data_file:
                shows_json = json.loads(data_file.read().decode("utf-8"))
            add_shows('DOCHD', shows_json)

        if 'SKYCRIC' in url_type:
            url = urllib.urlopen("http://192.168.0.160/sky.json")
            shows_json = json.loads(url.read().decode("utf-8"))
            add_shows(url_type, shows_json)

        if 'ZEM' in url_type:
            with open(json_path + 'zemshows.json') as data_file:
                shows_json = json.loads(data_file.read().decode("utf-8"))
            add_shows(url_type, shows_json)

        if 'SP' in url_type:
            with open(json_path + 'spkshows.json') as data_file:
                shows_json = json.loads(data_file.read().decode("utf-8"))
            add_shows(url_type, shows_json)

        if 'SMARTCRIC' in url_type:
            AddSmartCric(url_type)

        if 'refresh_shows' in url_type:
            shows_update()
    return


def AddSmartCric(url):
    import scdec
    channeladded = False
    for source in scdec.getlinks():
        add_directory(source[0], source[1], source[2], '', False, isItFolder=False)  # name,url,mode,icon
        channeladded = True

    if not channeladded:
        cname = 'No streams available'
        curl = ''
        add_directory('    -' + cname, curl, -1, '', False, isItFolder=False)  # name,url,mode,icon

    return


def add_shows(url_type, shows_json):
    shows_json = [x for x in shows_json if x != []]
    for i in range(0, len(shows_json)):
        if (shows_json[i]['Tag']) == url_type:
            link = {}
            Title = shows_json[i]['Title']
            icon = shows_json[i]['icon']
            link.update(shows_json[i]['link'])
            try:
                Title = h.unescape(Title).encode("utf-8")
            except:
                Title = re.sub(r'[\x80-\xFF]+', convert, Title)

            add_directory(Title.encode('utf-8'), link, 3, icon, True, isItFolder=False)

    return


def convert(s):
    try:
        return s.group(0).encode('latin1').decode('utf8')
    except:
        return s.group(0)


def play_showLink(name, linkType, video_id):
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
    listitem.setInfo("Video", {"Title": name})
    listitem.setProperty('mimetype', 'video/x-msvideo')
    listitem.setProperty('IsPlayable', 'true')

    if linkType == "SMARTCRIC":
        playlist.add(url, listitem)
        xbmcPlayer = xbmc.Player()
        xbmcPlayer.play(playlist)

    if linkType == "Playwire":
        import playwire
        media_url = playwire.resolve(video_id)
        playlist.add(media_url, listitem)
        xbmcgui.Dialog().notification(__addonname__, "Playing " + linkType + " video", __icon__, 3000, False)
        xbmc.Player().play(playlist)
        return

    import urlresolver
    if linkType == "DailyMotion":
        media_url = urlresolver.HostedMediaFile(host='dailymotion.com', media_id=video_id).resolve()
        playlist.add(media_url, listitem)
        xbmcgui.Dialog().notification(__addonname__, "Playing " + linkType + " video", __icon__, 3000, False)
        xbmc.Player().play(playlist)
    if linkType == "Youtube":
        media_url = urlresolver.HostedMediaFile(host='youtube.com', media_id=video_id).resolve()
        playlist.add(media_url, listitem)
        xbmcgui.Dialog().notification(__addonname__, "Playing " + linkType + " video", __icon__, 3000, False)
        xbmc.Player().play(playlist)
    if linkType == "Facebook":
        media_url = urlresolver.HostedMediaFile(host='facebook.com', media_id=video_id).resolve()
        playlist.add(media_url, listitem)
        xbmcgui.Dialog().notification(__addonname__, "Playing " + linkType + " video", __icon__, 3000, False)
        xbmc.Player().play(playlist)
    if linkType == "Openload":
        media_url = urlresolver.HostedMediaFile(host='openload.co', media_id=video_id).resolve()
        playlist.add(media_url, listitem)
        xbmcgui.Dialog().notification(__addonname__, "Playing " + linkType + " video", __icon__, 3000, False)
        xbmc.Player().play(playlist)

    return


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
    print('Script Starting...! ')
    print(datetime.datetime.now().time())
    spkshows(spk_url, spk_session)
    zemshows(zem_url, zem_session)
    print('Script Ended')
    print(datetime.datetime.now().time())


###

# Define function to monitor real time parameters ###
def get_params():
    param = []
    paramstring = sys.argv[2]
    print
    sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]

    return param


params = get_params()
url = None
name = None
mode = None
linkType = None
provider = None

# noinspection PyBroadException
try:
    url = urllib.unquote_plus(params["url"])
except:
    pass
# noinspection PyBroadException
try:
    name = urllib.unquote_plus(params["name"])
except:
    pass
# noinspection PyBroadException
try:
    mode = int(params["mode"])
except:
    pass

try:
    provider = urllib.unquote_plus(params["provider"])
except:
    pass

print
params
args = urlparse.parse_qs(sys.argv[2][1:])
# noinspection PyRedeclaration
linkType = ''

# noinspection PyBroadException
try:
    linkType = args.get('linkType', '')[0]
except:
    pass

print
name, mode, url, linkType, provider


# noinspection PyBroadException
try:
    if mode is None or url is None or len(url) < 1:
        add_types()
    elif mode == 2:
        add_enteries(url)
    elif mode == 3:
        play_showLink(name, provider, url)
    elif mode == 99:
        show_settings()

except:
    print
    'Something dint work'
    traceback.print_exc(file=sys.stdout)

if not (mode == 3):
    xbmcplugin.endOfDirectory(int(sys.argv[1]))