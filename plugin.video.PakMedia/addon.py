import HTMLParser
import base64
import cookielib
import os
import re
import sys
import traceback
import urllib
import urllib2
import urlparse
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
from multiprocessing.dummy import Pool
from multiprocessing import cpu_count
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

key = selfAddon.getSetting("url_key")
import pyaes as AES

cipher = AES.new(key, AES.MODE_ECB)
dts_url = cipher.decrypt(base64.b64decode(
    "gUhd9TxpnQppnZVAf7cv9oFIXfU8aZ0KaZ2VQH+3L/aBSF31PGmdCmmdlUB/ty/2gUhd9TxpnQppnZVAf7cv9nG7MNmOhZBiAocGtmWmCojQNzzg5WbretGM7yMoROvoeFdnCmkIyzLU1btJG5lmsUGKbZRy7yM2cNiQ/KpOgsU=")).strip(
    " ")
dv_url = cipher.decrypt(base64.b64decode(
    "gUhd9TxpnQppnZVAf7cv9oFIXfU8aZ0KaZ2VQH+3L/aBSF31PGmdCmmdlUB/ty/2gUhd9TxpnQppnZVAf7cv9o7+b9n9b+/gYKA7dux/WrB0buguCiDP0xozH/7K+mdJadTc2OjShMarfC9ZCZu+t396LLmkzHQol0iJVKz4y6E=")).strip(
    " ")
sc_url = cipher.decrypt(base64.b64decode(
    "gUhd9TxpnQppnZVAf7cv9oFIXfU8aZ0KaZ2VQH+3L/aBSF31PGmdCmmdlUB/ty/2gUhd9TxpnQppnZVAf7cv9uIn/fh/2pLiamYTTH2FXfnTf+epNapH/qM4oCYjVpg5EkKCfsgOLJDCTVhRAcqnChPgNMq3wmM5HtGGYBbXPlY=")).strip(
    " ")
zs_url = base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vY2F0ZWdvcnkvcGFraXN0YW5pLw==')
zv_url = base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vY2F0ZWdvcnkvdmlyYWwtdmlkZW9zLw==')

ZEMCOOKIEFILE = 'ZemCookieFile.lwp'
ZEMCOOKIEFILE = os.path.join(profile_path, ZEMCOOKIEFILE)

spicon = addonPath + '/resources/icon/siasatpk.png'
zmicon = addonPath + '/resources/icon/zem.jpg'

p_dm= re.compile("<iframe.*src=.*http.*dailymotion.com.*video[/](.*?)['|/?]")
p_yt= re.compile('<iframe.*?src=\".*?youtube.*?embed\/(.*?)[\"|\?]')
p_pw = re.compile('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"')
p_fb = re.compile('<.*["]http.*facebook[.]com[/]video[.]php[?]v[=](.*?)["]')

# Initializing the settings ###
if not selfAddon.getSetting("dummy") == "true":
    selfAddon.setSetting("dummy", "true")


# Define settting function ###
def show_settings():
    # type: () -> object
    selfAddon.openSettings()


# End of Addon Class info and setting ####

##### Define Functions #####
def add_types():
    add_directory('Daily Talk Shows', 'DTShows', 2, spicon)
    add_directory('Daily Vidoes', 'DVidoes', 2, spicon)
    add_directory('Sports Corner', 'SCorner', 2, spicon)
    add_directory('ZemTV Shows', 'ZS', 2, zmicon)
    add_directory('Zemtv Videos', 'ZV', 2, zmicon)
    add_directory('Settings', 'Settings', 99, 'OverlayZIP.png', isItFolder=False)
    return


def add_directory(name, url, mode, iconimage, showContext=False, isItFolder=True, linkType=None):
    if mode==3:
        u = sys.argv[0] + "?url=" + urllib.quote_plus(url.values()[0]) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&provider=" + url.keys()[0]
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


def add_enteries(name, url_type=None):
    if url_type == 'DTShows':
        add_shows(dts_url)
    elif url_type == 'DVidoes':
        add_shows(dv_url)
    elif url_type == 'SCorner':
        add_shows(sc_url)
    elif url_type == ('ZS'):
        addzemshows(zs_url)
    elif url_type == ('ZV'):
        addzemshows(zv_url)
    elif 'Next Page -' in name:
        add_shows(url_type)
    elif name == 'Next Page':
        addzemshows(url_type)
    return


def add_shows(Fromurl):
    headers = [('User-Agent',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
    link = getUrl(Fromurl, headers=headers)
    match = re.findall('<div class="threadinfo".*?<img src="(.*?)".*?href="(.*?)" id="thread_title.*?>(.*?)<', link,
                       re.DOTALL)

    try:
        pool = Pool(cpu_count()*2)
        pool.map(url_processor,match)
    finally:
        pool.close()
        pool.join()

    match = re.findall('title="Results.*?<a href="(.*?)" title', link, re.IGNORECASE)

    if len(match) > 0:
        pageurl = match[0]
        pg = ''
        try:
            if '/page' in pageurl:
                pg = pageurl.split('/page')[1].split('&')[0].split('/')[0]
        except:
            pass
        add_directory('Next Page - %s' % pg, 'http://www.siasat.pk/forum/' + pageurl, 2, '', isItFolder=True)
    return


def addzemshows(Fromurl):
    CookieJar = getZemCookieJar()
    headers = [('User-Agent',
                'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
    try:
        linkfull = getUrl(Fromurl, cookieJar=CookieJar, headers=headers)
    except:
        import cloudflare
        cloudflare.createCookie(Fromurl, CookieJar,
                                'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        linkfull = getUrl(Fromurl, cookieJar=CookieJar, headers=headers)
    pageNumber = 1
    catid = ''
    if not 'loopHandler' in Fromurl:
        catid = re.findall("currentcat = (.*?);", linkfull)[0]
        Fromurl = 'http://www.zemtv.com/wp-content/themes/zemresponsive/loopHandler.php?pageNumber=%s&catNumber=%s' % (
            str(pageNumber), catid)
        linkfull = getUrl(Fromurl, cookieJar=CookieJar, headers=headers)
    CookieJar.save(ZEMCOOKIEFILE, ignore_discard=True)
    match = re.findall('<div class=\"(?:teal)?.?card\">.*?<img src=\"(.*?)\".*?<a href=\"(.*?)\".*?>(.*?)<', linkfull,
                       re.UNICODE | re.DOTALL)

    try:
        pool = Pool(cpu_count()*2)
        pool.map(url_processor,match)
    finally:
        pool.close()
        pool.join()
    pageNumber = re.findall("pageNumber=(.*?)&", Fromurl)[0]
    catid = re.findall("catNumber=(.*)", Fromurl)[0]
    pageNumber = int(pageNumber) + 1
    Fromurl = 'http://www.zemtv.com/wp-content/themes/zemresponsive/loopHandler.php?pageNumber=%s&catNumber=%s' % (
        str(pageNumber), catid)
    add_directory('Next Page', Fromurl, 2, '', isItFolder=True)
    return


def getZemCookieJar(updatedUName=False):
    cookieJar = None
    try:
        cookieJar = cookielib.LWPCookieJar()
        if not updatedUName:
            cookieJar.load(ZEMCOOKIEFILE, ignore_discard=True)
    except:
        cookieJar = None
    if not cookieJar:
        cookieJar = cookielib.LWPCookieJar()
    return cookieJar


def getUrl(url, cookieJar=None, post=None, timeout=20, headers=None, jsonpost=False):
    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    header_in_page = None
    if '|' in url:
        url, header_in_page = url.split('|')
    req = urllib2.Request(url)
    req.add_header('User-Agent',
                   'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    req.add_header('Accept-Encoding', 'gzip')
    if headers:
        for h, hv in headers:
            req.add_header(h, hv)
    if header_in_page:
        header_in_page = header_in_page.split('&')
        for h in header_in_page:
            if len(h.split('=')) == 2:
                n, v = h.split('=')
            else:
                vals = h.split('=')
                n = vals[0]
                v = '='.join(vals[1:])
            req.add_header(n, v)
    if jsonpost:
        req.add_header('Content-Type', 'application/json')
    response = opener.open(req, post, timeout=timeout)
    if response.info().get('Content-Encoding') == 'gzip':
        from StringIO import StringIO
        import gzip
        buf = StringIO(response.read())
        f = gzip.GzipFile(fileobj=buf)
        link = f.read()
    else:
        link = response.read()
    response.close()
    return link


def convert(s):
    try:
        return s.group(0).encode('latin1').decode('utf8')
    except:
        return s.group(0)


def getCookiesString(cookieJar):
    try:
        cookieString = ""
        for index, cookie in enumerate(cookieJar):
            cookieString += cookie.name + "=" + cookie.value + ";"
    except:
        pass
    return cookieString


def get_showLink(name, url, linkType):
    headers = [('User-Agent',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
    link = getUrl(url, headers=headers)
    available_source = []
    available_link = []
    default_play = selfAddon.getSetting("DefaultVideoType")

    did = re.search(p_dm, link)
    if did:
        available_source.append("DailyMotion")
        available_link.append(did.groups(0))

    yid = re.search(p_yt, link)
    if yid:
        available_source.append("Youtube")
        available_link.append(yid.groups(0))

    fid = re.search(p_fb, link)
    if fid:
        available_source.append("Facebook")
        available_link.append(fid.groups(0))

    pid = re.search(p_pw, link)
    if pid:
        available_source.append("Playwire")
        available_link.append(pid.groups(0))

    if len(available_source) > 0:
        if linkType == "":
            if default_play in available_source:
                xbmcgui.Dialog().notification(__addonname__, "Playing " +default_play + " video", __icon__, 5000, False)
                play_showLink(name, default_play, available_link[available_source.index(default_play)])
                return
            else:
                xbmcgui.Dialog().notification(__addonname__, default_play+ " Video not found", __icon__, 2000, False)
                xbmcgui.Dialog().notification(__addonname__, "Playing " + available_source[0] + " video", __icon__, 2000, False)
                play_showLink(name, available_source[0], available_link[0])
                return

        else:
            if linkType in available_source:
                play_showLink(name, linkType, available_link[available_source.index(linkType)])
                return
            else:
                if linkType == "Checksrc":
                    if available_source is None:
                        xbmcgui.Dialog().ok(__addonname__, "No video link found in the post")
                        return
                    else:
                        dialog = xbmcgui.Dialog()
                        index = dialog.select("Available streams", available_source)
                        if index > -1:
                            play_showLink(name, available_source[index], available_link[index])
                            return
                        return
                xbmcgui.Dialog().ok(__addonname__, "No valid link found for " + linkType + " in the post")
                return
    xbmcgui.Dialog().ok(__addonname__, "No video link found in the post")
    return

def url_processor(cname):
    h = HTMLParser.HTMLParser()
    if 'zem' in cname[1]:
        tname = cname[2]
        url=cname[1]
        imageurl=cname[0]
        try:
            tname = h.unescape(tname).encode("utf-8")
        except:
            tname = re.sub(r'[\x80-\xFF]+', convert, tname)

    else:
        tname = cname[2]
        url = cname[1]
        imageurl = cname[0].replace('&amp;', '&')
        try:
            tname = h.unescape(tname).encode("utf-8")
        except:
            tname = re.sub(r'[\x80-\xFF]+', convert, tname)
        if not url.startswith('http'):
            url = 'http://www.siasat.pk/forum/' + url
        if not imageurl.startswith('http'):
            imageurl = 'http://www.siasat.pk/forum/' + url

    headers = [('User-Agent',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
    link = getUrl(url, headers=headers)

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

    if len(source) > 0:
        add_directory(tname, source, 3, imageurl, True, isItFolder=False)
    return


def play_showLink(name, linkType, video_id):
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
    listitem.setInfo("Video", {"Title": name})
    listitem.setProperty('mimetype', 'video/x-msvideo')
    listitem.setProperty('IsPlayable', 'true')

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

    return

# Define function to monitor real time parameters ###
def get_params():
    param = []
    paramstring = sys.argv[2]
    print sys.argv[2]
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
provider=None

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

print params
args = urlparse.parse_qs(sys.argv[2][1:])
# noinspection PyRedeclaration
linkType = ''

# noinspection PyBroadException
try:
    linkType = args.get('linkType', '')[0]
except:
    pass

print name,mode,url,linkType,provider

# noinspection PyBroadException
try:
    if mode is None or url is None or len(url) < 1:
        add_types()
    elif mode == 2:
        add_enteries(name, url)
    elif mode == 3:
        play_showLink(name, provider, url)
    elif mode == 99:
        show_settings()

except:
    print 'Something dint work'
    traceback.print_exc(file=sys.stdout)

if not (mode == 3):
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
