#
#
# Siasat.pk Kodi addon by Yasir
#
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
import urllib2
import urllib
import re
import traceback
import urlparse
import sys

# End of Imports

# Defining the Video URLs ####
Post_url = "http://www.siasat.pk/forum/showthread.php?"
Next_url = "http://www.siasat.pk/forum/"
DTS_url = "http://www.siasat.pk/forum/forumdisplay.php?29-Daily-Talk-Shows/"
DV_url = "http://www.siasat.pk/forum/forumdisplay.php?21-Siasi-Videos/"
SC_url = "http://www.siasat.pk/forum/forumdisplay.php?37-Sports-Corner/"
Isl_url = "http://www.siasat.pk/forum/forumdisplay.php?30-Islamic-Corner"
ST_url = "http://www.siasat.pk/forum/forumdisplay.php?39-Science-and-Technology"
Hl_url = "http://www.siasat.pk/forum/forumdisplay.php?42-Health-amp-Medical"

# Setting up basic Variables ####
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
    selfAddon.openSettings()


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


# Define function to add directory for each categories ###

def add_types():
    add_directory('Daily Talk Shows', 'DTShows', 2, '')
    add_directory('Daily Vidoes', 'DVidoes', 2, '')
    add_directory('Sports Corner', 'SCorner', 2, '')
    add_directory('Science and Technology', 'SCTC', 2, '')
    add_directory('Islamic Videos', 'Isl', 2, '')
    add_directory('Health and Medical', 'Hlmd', 2, '')
    add_directory('Settings', 'Settings', 99, '', isItFolder=False)

    return


# Define function to add directories with link ###
def add_directory(name, url, mode, iconimage, showContext=False, isItFolder=True, linkType=None):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    if showContext:
        cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "DailyMotion")
        cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "Youtube")
        liz.addContextMenuItems([('Play DailyMotion video', cmd1), ('Play Youtube video', cmd2)], replaceItems=True)

    if linkType:
        u = "XBMC.RunPlugin(%s&linkType=%s)" % (u, linkType)

    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isItFolder)
    return ok


def add_enteries(name, url_type=None):
    if url_type == 'DTShows':
        add_shows(DTS_url)
    elif url_type == 'DVidoes':
        add_shows(DV_url)
    elif url_type == 'SCorner':
        add_shows(SC_url)
    elif url_type == 'SCTC':
        add_shows(ST_url)
    elif url_type == 'Isl':
        add_shows(Isl_url)
    elif url_type == 'Hlmd':
        add_shows(Hl_url)
    elif name == 'Next Page':
        add_shows((Next_url + url))

    return


def add_shows(from_url):
    headers = {'User-Agent': 'Mozilla 5.10'}
    request = urllib2.Request(from_url, None, headers)
    response = urllib2.urlopen(request)
    link = response.read()

    show_url = re.compile('[<]a style.*id[=]["]thread_title_(.*)["][>]', re.IGNORECASE).findall(link)
    show_desc = re.compile('[<]a style.*["]\sid[=]["]thread.*["]>(.*)[<]').findall(link)
    show_img_list = re.compile('[<]img src[=]["](.*)["]\sstyle.*[>]').findall(link)
    show_img = []

    for i in show_img_list:
        show_img.append(re.sub("amp;", "", i))

    for urls, desc, img in zip(show_url, show_desc, show_img):
        add_directory(desc, urls, 3, img, showContext=True, isItFolder=True)

    match = re.findall('<span class="prev_next"><a rel="next" href="(.*)["]\stitle="Next Page', link, re.IGNORECASE)

    if len(match) == 2:
        add_directory('Next Page', match[0], 2, '', isItFolder=True)

    return


def get_showLink(url):
    global linkType
    headers = {'User-Agent': 'Mozilla 5.10'}
    request = urllib2.Request(url, None, headers)
    response = urllib2.urlopen(request)
    link = response.read()
    available_source = []
    available_link = []
    auto_play = selfAddon.getSetting("APlay")
    # noinspection PyUnusedLocal
    default_play = 0  # 0 DailyMotion, #1 Youtube
    default_play = selfAddon.getSetting("DefaultVideoType")

    did = re.findall('<iframe.*src=["]http.*dailymotion.com.*video[/](.*)[?].*["]', link)
    if did:
        available_source.append("DailyMotion")
        available_link.append(did[0])

    yid = re.findall('<iframe.*YouTube.*src=["].*youtube[.]com.*[/](.*)[?].*["].*iframe>', link)
    if yid:
        available_source.append("Youtube")
        available_link.append(yid[0])

    if len(available_source) > 0:
        if auto_play == "true":
            if default_play == "0":
                for i in available_source:
                    if i == "DailyMotion":
                        play_showLink(i, did[0])
                        return

            if default_play == "1":
                for i in available_source:
                    if i == "Youtube":
                        play_showLink(i, yid[0])
                        return

            xbmcgui.Dialog().ok(__addonname__, "No Valid Link Available for Default Play Source")

        dialog = xbmcgui.Dialog()
        index = dialog.select('Choose your stream', available_source)

        if index > -1:
            linkType = available_source[index]
            linkurl = available_link[index]

        if linkType:
            # noinspection PyUnboundLocalVariable
            play_showLink(linkType, linkurl)

    else:
        xbmcgui.Dialog().ok(__addonname__, "No Valid link found in the post")

    return


def play_showLink(name, video_id):
    if name == "DailyMotion":
        xbmc.executebuiltin('PlayMedia(plugin://plugin.video.dailymotion/?url=' + video_id + '&mode=playVideo)')

    if name == "Youtube":
        xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id=' + video_id + ')')

    return


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
        add_types()

    elif mode == 2:
        add_enteries(name, url)

    elif mode == 3:
        get_showLink(Post_url + url)

    elif mode == 99:
        show_settings()

except:
    print 'Something dint work'
    traceback.print_exc(file=sys.stdout)

if not (mode == 3):
    xbmcplugin.endOfDirectory(int(sys.argv[1]))