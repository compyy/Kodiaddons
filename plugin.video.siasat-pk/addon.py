#
# Siasat.pk Kodi addon by Yasir
#
# Importing required modules ####
# noinspection PyUnresolvedReferences
import xbmc
# noinspection PyUnresolvedReferences
import xbmcgui
# noinspection PyUnresolvedReferences
import xbmcplugin
# noinspection PyUnresolvedReferences
import xbmcaddon
# noinspection PyUnresolvedReferences
import urlresolver
import urllib2
import urllib
import re
import traceback
import urlparse
import sys
from Crypto.Cipher import AES
import base64

#
# End of Imports
#
# Setting up basic Variables for XBMC ####
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.siasat-pk'
selfAddon = xbmcaddon.Addon(id=addon_id)
profile_path = xbmc.translatePath(selfAddon.getAddonInfo('profile'))

addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonversion = xbmcaddon.Addon().getAddonInfo("version")

# Initializing the settings ###
if not selfAddon.getSetting("dummy") == "true":
    selfAddon.setSetting("dummy", "true")


# Define settting function ###
def show_settings():
    # type: () -> object
    selfAddon.openSettings()


# End of Addon Class info and setting ####

class Video:
    def __init__(self):
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
        self.isl_url = cipher.decrypt(base64.b64decode(
            "gUhd9TxpnQppnZVAf7cv9oFIXfU8aZ0KaZ2VQH+3L/aBSF31PGmdCmmdlUB/ty/2gUhd9TxpnQppnZVAf7cv9uIn/fh/2pLiamYTTH2FXfnTf+epNapH/qM4oCYjVpg5EkKCfsgOLJDCTVhRAcqnCp4QUloS7+YNJ7fJI8LkirI=")).strip(
            " ")
        self.st_url = cipher.decrypt(base64.b64decode(
            "gUhd9TxpnQppnZVAf7cv9oFIXfU8aZ0KaZ2VQH+3L/aBSF31PGmdCmmdlUB/ty/23N9Zk2e8ronI87UoNwKFn27yaRWS072GBmYitb5S9Ta1WhVHMG7aT3+wZn+ag7G4wCFlUvgDKSgUe0O2RZ5ECAuWa5cmfR7trgsPVOn+3v0=")).strip(
            " ")
        self.hm_url = cipher.decrypt(base64.b64decode(
            "gUhd9TxpnQppnZVAf7cv9oFIXfU8aZ0KaZ2VQH+3L/aBSF31PGmdCmmdlUB/ty/2CQd68kAxB14rfpsCAfmCIhTyLCCYq6Yomt0sY2USTc+F7X2pz6iwdyf0pDwigbeadoy6whtYBaL8op6Swshw3klxcH8ukbqp0vKJqlrudHI=")).strip(
            " ")

    def add_types(self):
        self.add_directory('Daily Talk Shows', 'DTShows', 2, '')
        self.add_directory('Daily Vidoes', 'DVidoes', 2, '')
        self.add_directory('Sports Corner', 'SCorner', 2, '')
        self.add_directory('Science and Technology', 'SCTC', 2, '')
        self.add_directory('Islamic Videos', 'Isl', 2, '')
        self.add_directory('Health and Medical', 'Hlmd', 2, '')
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
            cmd4 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "Checksrc")
            liz.addContextMenuItems(
                [('Play DailyMotion video', cmd1), ('Play Youtube video', cmd2), ('Play Facebook video', cmd3),
                 ('Check Available Sources', cmd4)],
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
        elif url_type == 'SCTC':
            self.add_shows(self.st_url)
        elif url_type == 'Isl':
            self.add_shows(self.isl_url)
        elif url_type == 'Hlmd':
            self.add_shows(self.hm_url)
        elif name == 'Next Page':
            self.add_shows((self.next_url + url))

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

    def get_showLink(self, url):
        global linkType
        headers = {'User-Agent': 'Mozilla 5.10'}
        request = urllib2.Request(url, None, headers)
        response = urllib2.urlopen(request)
        link = response.read()
        available_source = []
        available_link = []
        default_play = selfAddon.getSetting("DefaultVideoType")

        did = re.findall('<iframe.*src=["]http.*dailymotion.com.*video[/](.*)[?].*["]', link)
        if did:
            available_source.append("DailyMotion")
            available_link.append(did[0])

        yid = re.findall('<iframe.*YouTube.*src=["].*youtube[.]com.*[/](.*)[?].*["].*iframe>', link)
        if yid:
            available_source.append("Youtube")
            available_link.append(yid[0])

        fid = re.findall('<.*["]http.*facebook[.]com[/]video[.]php[?]v[=](.*?)["]', link)
        if fid:
            available_source.append("Facebook")
            available_link.append(fid[0])

        if len(available_source) > 0:
            if linkType == "":
                if default_play in available_source:
                    self.play_showLink(default_play, available_link[available_source.index(default_play)])
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
                            xbmcgui.Dialog().ok(__addonname__, "No video link found in the post")
                            return
                        else:
                            dialog = xbmcgui.Dialog()
                            index = dialog.select("Available streams", available_source)
                            if index > -1:
                                self.play_showLink(available_source[index], available_link[index])
                                return

                    xbmcgui.Dialog().ok(__addonname__, "No valid link found for " + linkType + " in the post")
                    return

        xbmcgui.Dialog().ok(__addonname__, "No video link found in the post")
        return

    def play_showLink(self, name, video_id):
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

# Initializing Video Instance
v = Video()

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

args = urlparse.parse_qs(sys.argv[2][1:])
# noinspection PyRedeclaration
linkType = ''

# noinspection PyBroadException
try:
    linkType = args.get('linkType', '')[0]
except:
    pass

print mode, url, name, linkType

# noinspection PyBroadException
try:
    if mode is None or url is None or len(url) < 1:
        v.add_types()

    elif mode == 2:
        v.add_enteries(name, url)

    elif mode == 3:
        v.get_showLink(v.post_url + url)

    elif mode == 99:
        show_settings()

except:
    print 'Something dint work'
    traceback.print_exc(file=sys.stdout)

if not (mode == 3):
    xbmcplugin.endOfDirectory(int(sys.argv[1]))
