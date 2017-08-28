#
# Siasat.pk Kodi addon by Yasir
#
# Importing required modules ####
# noinspection PyUnresolvedReferences
import HTMLParser
import base64
import cookielib
import os
import re
import sys
import urllib
import urllib2

import pyaes as AES
import xbmc
# noinspection PyUnresolvedReferences
import xbmcaddon
# noinspection PyUnresolvedReferences
import xbmcgui
# noinspection PyUnresolvedReferences
import xbmcplugin


class Siasat:
    def __init__(self, __addon__, __addonname__, __icon__, addon_id, selfAddon, profile_path, addonPath, addonversion,
                 ZEMCOOKIEFILE):
        key = selfAddon.getSetting("url_key")
        cipher = AES.new(key, AES.MODE_ECB)
        self.post_url = cipher.decrypt(base64.b64decode(
            "gUhd9TxpnQppnZVAf7cv9oFIXfU8aZ0KaZ2VQH+3L/aBSF31PGmdCmmdlUB/ty/2gUhd9TxpnQppnZVAf7cv9oFIXfU8aZ0KaZ2VQH+3L/b6BmZZqrhlL4SKcYirKTo2ASgtvWqodYWYeV/fYUG+fZg2Im9fqsVvGRsTKHcY6Pc=")).strip(
            " ")
        self.next_url = cipher.decrypt(base64.b64decode(
            "gUhd9TxpnQppnZVAf7cv9oFIXfU8aZ0KaZ2VQH+3L/aBSF31PGmdCmmdlUB/ty/2gUhd9TxpnQppnZVAf7cv9oFIXfU8aZ0KaZ2VQH+3L/aBSF31PGmdCmmdlUB/ty/2wsQCVFMpAUbOB+rHQzsBdUux7PwjhymHQMHFmWH8+T4=")).strip(
            " ")
        self.dts_url = cipher.decrypt(base64.b64decode(
            "gUhd9TxpnQppnZVAf7cv9oFIXfU8aZ0KaZ2VQH+3L/aBSF31PGmdCmmdlUB/ty/2gUhd9TxpnQppnZVAf7cv9nG7MNmOhZBiAocGtmWmCojQNzzg5WbretGM7yMoROvoeFdnCmkIyzLU1btJG5lmsUGKbZRy7yM2cNiQ/KpOgsU=")).strip(
            " ")
        self.dv_url = cipher.decrypt(base64.b64decode(
            "gUhd9TxpnQppnZVAf7cv9oFIXfU8aZ0KaZ2VQH+3L/aBSF31PGmdCmmdlUB/ty/2gUhd9TxpnQppnZVAf7cv9o7+b9n9b+/gYKA7dux/WrB0buguCiDP0xozH/7K+mdJadTc2OjShMarfC9ZCZu+t396LLmkzHQol0iJVKz4y6E=")).strip(
            " ")
        self.sc_url = cipher.decrypt(base64.b64decode(
            "gUhd9TxpnQppnZVAf7cv9oFIXfU8aZ0KaZ2VQH+3L/aBSF31PGmdCmmdlUB/ty/2gUhd9TxpnQppnZVAf7cv9uIn/fh/2pLiamYTTH2FXfnTf+epNapH/qM4oCYjVpg5EkKCfsgOLJDCTVhRAcqnChPgNMq3wmM5HtGGYBbXPlY=")).strip(
            " ")
        self.zs_url = base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vY2F0ZWdvcnkvcGFraXN0YW5pLw==')
        self.zv_url = base64.b64decode('aHR0cDovL3d3dy56ZW10di5jb20vY2F0ZWdvcnkvdmlyYWwtdmlkZW9zLw==')

        self.__addon__ = __addon__
        self.__addonname__ = __addonname__
        self.__icon__ = __icon__
        self.addon_id = addon_id
        self.selfAddon = selfAddon
        self.profile_path = profile_path
        self.addonPath = addonPath
        self.addonversion = addonversion
        self.spicon = self.addonPath + "/resources/icon/siasatpk.png"
        self.zmicon = self.addonPath + "/resources/icon/zem.jpg"
        self.ZEMCOOKIEFILE = ZEMCOOKIEFILE

    def add_types(self):
        self.add_directory('Daily Talk Shows', 'DTShows', 2, self.spicon)
        self.add_directory('Daily Vidoes', 'DVidoes', 2, self.spicon)
        self.add_directory('Sports Corner', 'SCorner', 2, self.spicon)
        self.add_directory('ZemTV Shows', 'ZS', 2, self.zmicon)
        self.add_directory('Zemtv Videos', 'ZV', 2, self.zmicon)
        self.add_directory('Settings', 'Settings', 99, 'OverlayZIP.png', isItFolder=False)

        return

    def add_directory(self, name, url, mode, iconimage, showContext=False, isItFolder=True, linkType=None):
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

    def add_enteries(self, name, url_type=None):
        if url_type == 'DTShows':
            self.add_shows(self.dts_url)
        elif url_type == 'DVidoes':
            self.add_shows(self.dv_url)
        elif url_type == 'SCorner':
            self.add_shows(self.sc_url)
        elif url_type == ('ZS'):
            self.addzemshows(self.zs_url)
        elif url_type == ('ZV'):
            self.addzemshows(self.zv_url)
        elif name == 'Next Page':
            self.add_shows((self.next_url + url_type))
        elif name == 'Zem Next Page':
            self.addzemshows(url_type)
        return

    def add_shows(self, from_url):
        # Opening a HTTP session to load videos
        headers = {'User-Agent': 'Mozilla 5.10'}
        request = urllib2.Request(from_url, None, headers)
        response = urllib2.urlopen(request)

        # Using re.sub to clear the links from amp;
        link = re.sub("amp;", "", response.read())

        # filtering the input and filtering the links.
        show_url = re.compile('[<]a style.*id[=]["]thread_title_(.*)["][>]', re.IGNORECASE).findall(link)
        show_desc = re.compile('[<]a style.*["]\sid[=]["]thread.*["]>(.*)[<]').findall(link)
        show_img = re.compile('[<]img src[=]["](.*)["]\sstyle.*[>]').findall(link)

        # Using zip for  iterables into pairwise tuples
        for urls, desc, img in zip(show_url, show_desc, show_img):
            self.add_directory(desc, urls, 3, img, showContext=True, isItFolder=True)

        match = re.findall('<span class="prev_next"><a rel="next" href="(.*)["]\stitle="Next Page', link, re.IGNORECASE)

        if len(match) == 2:
            self.add_directory('Next Page', match[0], 2, '', isItFolder=True)

        return

    def addzemshows(self, Fromurl):
        CookieJar = self.getZemCookieJar()
        headers = [('User-Agent',
                    'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
        try:
            linkfull = self.getUrl(Fromurl, cookieJar=CookieJar, headers=headers)
        except:
            import cloudflare
            cloudflare.createCookie(Fromurl, CookieJar,'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
            linkfull = self.getUrl(Fromurl, cookieJar=CookieJar, headers=headers)

        pageNumber = 1
        catid = ''

        if not 'loopHandler' in Fromurl:
            catid = re.findall("currentcat = (.*?);",linkfull)[0]
            Fromurl = 'http://www.zemtv.com/wp-content/themes/zemresponsive/loopHandler.php?pageNumber=%s&catNumber=%s'%(str(pageNumber), catid)
            linkfull = self.getUrl(Fromurl, cookieJar=CookieJar, headers=headers)

        CookieJar.save(self.ZEMCOOKIEFILE, ignore_discard=True)
        match = re.findall('<div class=\"(?:teal)?.?card\">.*?<img src=\"(.*?)\".*?<a href=\"(.*?)\".*?>(.*?)<', linkfull, re.UNICODE | re.DOTALL)
        print match
        h = HTMLParser.HTMLParser()

        for cname in match:
            tname = cname[2]
            try:
                tname = h.unescape(tname).encode("utf-8")
            except:
                tname = re.sub(r'[\x80-\xFF]+', self.convert, tname)

            self.add_directory(tname, cname[1], 4, cname[0] + '|Cookie=%s' % self.getCookiesString(
                CookieJar) + '&User-Agent=Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10',
                               True, isItFolder=False)

        pageNumber = re.findall("pageNumber=(.*?)&", Fromurl)[0]
        catid = re.findall("catNumber=(.*)", Fromurl)[0]

        pageNumber = int(pageNumber) + 1
        Fromurl = 'http://www.zemtv.com/wp-content/themes/zemresponsive/loopHandler.php?pageNumber=%s&catNumber=%s' % (
        str(pageNumber), catid)
        self.add_directory('Zem Next Page', Fromurl, 2, '', isItFolder=True)
        return

    def getZemCookieJar(updatedUName=False):
        cookieJar = None
        try:
            cookieJar = cookielib.LWPCookieJar()
            if not updatedUName:
                cookieJar.load(self.ZEMCOOKIEFILE, ignore_discard=True)
        except:
            cookieJar = None

        if not cookieJar:
            cookieJar = cookielib.LWPCookieJar()
        return cookieJar

    def getUrl(self, url, cookieJar=None, post=None, timeout=20, headers=None, jsonpost=False):
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

    def convert(self, s):
        try:
            return s.group(0).encode('latin1').decode('utf8')
        except:
            return s.group(0)

    def getCookiesString(self, cookieJar):
        try:
            cookieString = ""
            for index, cookie in enumerate(cookieJar):
                cookieString += cookie.name + "=" + cookie.value + ";"
        except:
            pass
        return cookieString

    def get_showLink(self, url, linkType,type):
        headers = {'User-Agent': 'Mozilla 5.10'}
        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)
        link = response.read()
        available_source = []
        available_link = []
        default_play = self.selfAddon.getSetting("DefaultVideoType")

        if type=='siasat':
            did = re.findall('<iframe.*src=["]http.*dailymotion.com.*video[/](.*)[?].*["]', link)
        elif type=='zemtv':
            did = re.findall("<iframe.*src=[']http.*dailymotion.com.*video[/](.*?)[']", link)
        if did:
            available_source.append("DailyMotion")
            available_link.append(did[0])

        if type=='siasat':
            yid = re.findall('<iframe.*YouTube.*src=["].*youtube[.]com.*[/](.*)[?].*["].*iframe>', link)
        elif type=='zemtv':
            yidre.findall('<iframe.*?src=\".*?youtube.*?embed\/(.*?)\"', link, re.DOTALL | re.IGNORECASE)
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
                    self.play_showLink(default_play, available_link[available_source.index(default_play)])
                    return
                else:
                    if default_play == "":
                        xbmcgui.Dialog().ok(self.__addonname__, "Default Player has been initialized to DailyMotion")
                        default_play = "DailyMotion"

                    dialog = xbmcgui.Dialog()
                    index = dialog.select(
                        "No valid link available for " + default_play + " Source\nChoose from available stream",
                        available_source)
                    if index > -1:
                        self.play_showLink(available_source[index], available_link[index])
                        return

                    else:
                        return
            else:
                if linkType in available_source:
                    self.play_showLink(linkType, available_link[available_source.index(linkType)])
                    return

                else:
                    if linkType == "Checksrc":
                        if available_source is None:
                            xbmcgui.Dialog().ok(self.__addonname__, "No video link found in the post")
                            return
                        else:
                            dialog = xbmcgui.Dialog()
                            index = dialog.select("Available streams", available_source)
                            if index > -1:
                                self.play_showLink(available_source[index], available_link[index])
                                return
                            return

                    xbmcgui.Dialog().ok(self.__addonname__, "No valid link found for " + linkType + " in the post")
                    return

        xbmcgui.Dialog().ok(self.__addonname__, "No video link found in the post")
        return

    def play_showLink(self, name, video_id):

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