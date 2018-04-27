import base64
import re

import HTMLParser
import urllib2

dts_url = base64.b64decode('aHR0cDovL3d3dy5zaWFzYXQucGsvZm9ydW0vZm9ydW1kaXNwbGF5LnBocD8yOS1EYWlseS1UYWxrLVNob3dzLw==')
dv_url = base64.b64decode('aHR0cDovL3d3dy5zaWFzYXQucGsvZm9ydW0vZm9ydW1kaXNwbGF5LnBocD8yMS1TaWFzaS1WaWRlb3Mv')
sc_url = base64.b64decode('aHR0cDovL3d3dy5zaWFzYXQucGsvZm9ydW0vZm9ydW1kaXNwbGF5LnBocD8zNy1TcG9ydHMtQ29ybmVyLw==')
zs_url = base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vY2F0ZWdvcnkvcGFraXN0YW5pLw==')
zv_url = base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vY2F0ZWdvcnkvdmlyYWwtdmlkZW9zLw==')

ZEMCOOKIEFILE = 'ZemCookieFile.lwp'

p_dm = re.compile("<iframe.*src=.*http.*dailymotion.com.*video[/](.*?)['|/?]")
p_yt = re.compile('<iframe.*?src=\".*?youtube.*?embed\/(.*?)[\"|\?]')
p_pw = re.compile('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"')
p_fb = re.compile('<.*["]http.*facebook[.]com[/]video[.]php[?]v[=](.*?)["]')


def add_shows(dts_url):
    headers = [('User-Agent',
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
    link = getUrl(dts_url, headers=headers)
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

        print(tname, url, imageurl)


#
# def addzemshows(Fromurl):
#     CookieJar = getZemCookieJar()
#     headers = [('User-Agent',
#                 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
#     try:
#         linkfull = getUrl(Fromurl, cookieJar=CookieJar, headers=headers)
#     except:
#         import cloudflare
#         cloudflare.createCookie(Fromurl, CookieJar,
#                                 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
#         linkfull = getUrl(Fromurl, cookieJar=CookieJar, headers=headers)
#     pageNumber = 1
#     catid = ''
#     if not 'loopHandler' in Fromurl:
#         catid = re.findall("currentcat = (.*?);", linkfull)[0]
#         Fromurl = 'http://www.zemtv.com/wp-content/themes/zemresponsive/loopHandler.php?pageNumber=%s&catNumber=%s' % (
#             str(pageNumber), catid)
#         linkfull = getUrl(Fromurl, cookieJar=CookieJar, headers=headers)
#     CookieJar.save(ZEMCOOKIEFILE, ignore_discard=True)
#     match = re.findall('<div class=\"(?:teal)?.?card\">.*?<img src=\"(.*?)\".*?<a href=\"(.*?)\".*?>(.*?)<', linkfull,
#                        re.UNICODE | re.DOTALL)
#     print match
#     h = HTMLParser.HTMLParser()
#     for cname in match:
#         tname = cname[2]
#         try:
#             tname = h.unescape(tname).encode("utf-8")
#         except:
#             tname = re.sub(r'[\x80-\xFF]+', convert, tname)
#         add_directory(tname, cname[1], 3, cname[0] + '|Cookie=%s' % getCookiesString(
#             CookieJar) + '&User-Agent=Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10',
#                       True, isItFolder=False)
#     pageNumber = re.findall("pageNumber=(.*?)&", Fromurl)[0]
#     catid = re.findall("catNumber=(.*)", Fromurl)[0]
#     pageNumber = int(pageNumber) + 1
#     Fromurl = 'http://www.zemtv.com/wp-content/themes/zemresponsive/loopHandler.php?pageNumber=%s&catNumber=%s' % (
#         str(pageNumber), catid)
#     add_directory('Next Page', Fromurl, 2, '', isItFolder=True)
#     return
#
#
# def getZemCookieJar(updatedUName=False):
#     cookieJar = None
#     try:
#         cookieJar = cookielib.LWPCookieJar()
#         if not updatedUName:
#             cookieJar.load(ZEMCOOKIEFILE, ignore_discard=True)
#     except:
#         cookieJar = None
#     if not cookieJar:
#         cookieJar = cookielib.LWPCookieJar()
#     return cookieJar
#
#
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
#
#
# def get_showLink(name, url, linkType):
#     headers = [('User-Agent',
#                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36')]
#     link = getUrl(url, headers=headers)
#     available_source = []
#     available_link = []
#     default_play = selfAddon.getSetting("DefaultVideoType")
#
#     did = re.search(p_dm, link)
#     if did:
#         available_source.append("DailyMotion")
#         available_link.append(did.groups(0))
#
#     yid = re.search(p_yt, link)
#     if yid:
#         available_source.append("Youtube")
#         available_link.append(yid.groups(0))
#
#     fid = re.search(p_fb, link)
#     if fid:
#         available_source.append("Facebook")
#         available_link.append(fid.groups(0))
#
#     pid = re.search(p_pw, link)
#     if pid:
#         available_source.append("Playwire")
#         available_link.append(pid.groups(0))
#
#     if len(available_source) > 0:
#         if linkType == "":
#             if default_play in available_source:
#                 xbmcgui.Dialog().notification(__addonname__, "Playing " +default_play + " video", __icon__, 5000, False)
#                 play_showLink(name, default_play, available_link[available_source.index(default_play)])
#                 return
#             else:
#                 xbmcgui.Dialog().notification(__addonname__, default_play+ " Video not found", __icon__, 2000, False)
#                 xbmcgui.Dialog().notification(__addonname__, "Playing " + available_source[0] + " video", __icon__, 2000, False)
#                 play_showLink(name, available_source[0], available_link[0])
#                 return
#
#         else:
#             if linkType in available_source:
#                 play_showLink(name, linkType, available_link[available_source.index(linkType)])
#                 return
#             else:
#                 if linkType == "Checksrc":
#                     if available_source is None:
#                         xbmcgui.Dialog().ok(__addonname__, "No video link found in the post")
#                         return
#                     else:
#                         dialog = xbmcgui.Dialog()
#                         index = dialog.select("Available streams", available_source)
#                         if index > -1:
#                             play_showLink(name, available_source[index], available_link[index])
#                             return
#                         return
#                 xbmcgui.Dialog().ok(__addonname__, "No valid link found for " + linkType + " in the post")
#                 return
#     xbmcgui.ialog().ok(__addonname__, "No video link found in the post")
#     return
#
#
#
# p = Pool(10)
# records = p.map(parse, cars_links)
# p.terminate()
# p.join()
