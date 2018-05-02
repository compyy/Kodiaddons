import json
import os
import re
import sys
import traceback
import urllib

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

spicon = addonPath + '/resources/icon/siasatpk.png'
docicon = addonPath + '/resources/icon/docu.png'
zmicon = addonPath + '/resources/icon/zem.jpg'
docshowjson = addonPath + '/resources/lib/'


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
            url = urllib.urlopen("http://compysc.westus2.cloudapp.azure.com/docshows.json")
            shows_json = json.loads(url.read().decode("utf-8"))
            add_shows(url_type, shows_json)

        if 'DOCHDOLD' in url_type:
            with open(docshowjson + 'docshowsold.json') as data_file:
                shows_json = json.loads(data_file.read().decode("utf-8"))
            add_shows('DOCHD', shows_json)

        else:
            url = urllib.urlopen("http://compysc.westus2.cloudapp.azure.com/shows.json")
            shows_json = json.loads(url.read().decode("utf-8"))
            add_shows(url_type, shows_json)
    return


def add_shows(url_type, shows_json):
    shows_json = [x for x in shows_json if x != []]
    print(len(shows_json))
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