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
    h = HTMLParser.HTMLParser()

    for cname in match:
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

        add_directory(tname, url, 3, imageurl, True, isItFolder=False)

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
    print match
    h = HTMLParser.HTMLParser()
    for cname in match:
        tname = cname[2]
        try:
            tname = h.unescape(tname).encode("utf-8")
        except:
            tname = re.sub(r'[\x80-\xFF]+', convert, tname)
        add_directory(tname, cname[1], 4, cname[0] + '|Cookie=%s' % getCookiesString(
            CookieJar) + '&User-Agent=Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10',
                      True, isItFolder=False)
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


def get_showLink(url, linkType, type):
    headers = {'User-Agent': 'Mozilla 5.10'}
    request = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request)
    link = response.read()
    available_source = []
    available_link = []
    default_play = selfAddon.getSetting("DefaultVideoType")
    if type == 'siasat':
        did = re.findall('<iframe.*src=["]http.*dailymotion.com.*video[/](.*)[?].*["]', link)
    elif type == 'zemtv':
        did = re.findall("<iframe.*src=[']http.*dailymotion.com.*video[/](.*?)[']", link)
    if did:
        available_source.append("DailyMotion")
        available_link.append(did[0])

    if type == 'siasat':
        yid = re.findall('<iframe.*YouTube.*src=["].*youtube[.]com.*[/](.*)[?].*["].*iframe>', link)
    elif type == 'zemtv':
        yid = re.findall('<iframe.*?src=\".*?youtube.*?embed\/(.*?)\"', link, re.DOTALL | re.IGNORECASE)
    if yid:
        available_source.append("Youtube")
        available_link.append(yid[0])

    fid = re.findall('<.*["]http.*facebook[.]com[/]video[.]php[?]v[=](.*?)["]', link)
    if fid:
        available_source.append("Facebook")
        available_link.append(fid[0])

    pid = re.findall('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"', link)
    if len(pid) == 0:
        pid = re.findall('data-config="(.*?config.playwire.com.*?)"', link)
    if pid:
        available_source.append("Playwire")
        available_link.append(pid[0])

    if len(available_source) > 0:
        if linkType == "":
            if default_play in available_source:
                play_showLink(default_play, available_link[available_source.index(default_play)])
                return
            else:
                if default_play == "":
                    xbmcgui.Dialog().ok(__addonname__, "Default Player has been initialized to DailyMotion")
                    default_play = "DailyMotion"
                dialog = xbmcgui.Dialog()
                index = dialog.select(
                    "No valid link available for " + default_play + " Source\nChoose from available stream",
                    available_source)
                if index > -1:
                    play_showLink(available_source[index], available_link[index])
                    return
                else:
                    return
        else:
            if linkType in available_source:
                play_showLink(linkType, available_link[available_source.index(linkType)])
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
                            play_showLink(available_source[index], available_link[index])
                            return
                        return
                xbmcgui.Dialog().ok(__addonname__, "No valid link found for " + linkType + " in the post")
                return
    xbmcgui.Dialog().ok(__addonname__, "No video link found in the post")
    return


def play_showLink(name, video_id):
    if name == "Playwire":
        import playwire
        media_url = playwire.resolve(video_id)
        # media_url = urlresolver.HostedMediaFile(host='facebook.com', media_id=video_id).resolve()
        xbmc.Player().play(media_url)
        return
    # noinspection PyUnresolvedReferences
    import urlresolver
    if name == "DailyMotion":
        media_url = urlresolver.HostedMediaFile(host='dailymotion.com', media_id=video_id).resolve()
        xbmc.Player().play(media_url)
    if name == "Youtube":
        media_url = urlresolver.HostedMediaFile(host='youtube.com', media_id=video_id).resolve()
        xbmc.Player().play(media_url)
    if name == "Facebook":
        media_url = urlresolver.HostedMediaFile(host='facebook.com', media_id=video_id).resolve()
        xbmc.Player().play(media_url)
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

print params
args = urlparse.parse_qs(sys.argv[2][1:])
# noinspection PyRedeclaration
linkType = ''

# noinspection PyBroadException
try:
    linkType = args.get('linkType', '')[0]
except:
    pass

print name,mode,url,linkType

# noinspection PyBroadException
try:
    if mode is None or url is None or len(url) < 1:
        add_types()
    elif mode == 2:
        add_enteries(name, url)
    elif mode == 3:
        get_showLink(url, linkType, type='siasat')
    elif mode == 4:
        get_showLink(url, linkType, type='zemtv')
    elif mode == 99:
        show_settings()

except:
    print 'Something dint work'
    traceback.print_exc(file=sys.stdout)

if not (mode == 3):
    xbmcplugin.endOfDirectory(int(sys.argv[1]))