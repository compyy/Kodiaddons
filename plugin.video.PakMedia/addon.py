import json
import os
import sys
import time
import traceback
from urllib.parse import quote_plus, parse_qs, unquote_plus

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin
import xbmcvfs

# End of Imports
#
# Setting up basic Variables for XBMC ####
__addon__ = xbmcaddon.Addon()
__addonname__ = __addon__.getAddonInfo('name')
__icon__ = __addon__.getAddonInfo('icon')

addon_id = 'plugin.video.PakMedia'
selfAddon = xbmcaddon.Addon(id=addon_id)
profile_path = xbmcvfs.translatePath(selfAddon.getAddonInfo('profile'))
addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonversion = xbmcaddon.Addon().getAddonInfo("version")
sys.path.append(os.path.join(addonPath, 'resources', 'lib'))

spicon = addonPath + '/resources/icon/siasatpk.png'
json_path = addonPath + '/resources/json/'
service_addon = addonPath + '/service.py'

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
    add_directory('Refresh Shows', 'refresh_shows', 2, '')
    add_directory('Settings', 'Settings', 99, 'OverlayZIP.png', isItFolder=False)
    return


def add_directory(name, url, mode, iconimage, isItFolder=True, linkType=None):
    if mode == 3:
        u = sys.argv[0] + "?url=" + quote_plus(list(url.values())[0]) + "&mode=" + str(
            mode) + "&name=" + quote_plus(name) + "&provider=" + list(url.keys())[0]
    else:
        u = sys.argv[0] + "?url=" + quote_plus(url) + "&mode=" + str(mode) + "&name=" + quote_plus(name)

    liz = xbmcgui.ListItem(name)
    liz.setArt({"icon": "DefaultFolder.png", "thumb": iconimage})
    liz.setInfo(type="Video", infoLabels={"Title": name})
    if linkType:
        u = "XBMC.RunPlugin(%s&linkType=%s)" % (u, linkType)
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=isItFolder)
    return ok


def add_enteries(url_type=None):
    if url_type:
        if 'SP' in url_type:
            with open(json_path + 'spkshows.json', encoding='utf-8') as data_file:
                shows_json = json.loads(data_file.read())
            add_shows(url_type, shows_json)

        if 'refresh_shows' in url_type:
            xbmc.executebuiltin('XBMC.RunScript(' + service_addon + ')')

    return


def add_shows(url_type, shows_json):
    shows_json = [x for x in shows_json if x != []]
    for i in range(0, len(shows_json)):
        if (shows_json[i]['Tag']) == url_type:
            link = {}
            Title = shows_json[i]['Title']
            icon = shows_json[i]['icon']
            link.update(shows_json[i]['link'])
            print(Title, icon, link)
            add_directory(Title, link, 3, icon, isItFolder=False)

    return


def convert(s):
    try:
        return s.group(0).encode('latin1').decode('utf8')
    except:
        return s.group(0)


def play_showLink(name, linkType, video_id):
    playlist = xbmc.PlayList(1)
    playlist.clear()
    listitem = xbmcgui.ListItem(name)
    listitem.setArt({"icon": "DefaultFolder.png"})
    listitem.setInfo("Video", {"Title": name})
    listitem.setProperty('mimetype', 'video/x-msvideo')
    listitem.setProperty('IsPlayable', 'true')

    if linkType == "Playwire":
        xbmcgui.Dialog().notification(__addonname__, "Playing " + linkType + " video", __icon__, 3000, False)
        import playwire
        media_url = playwire.resolve(video_id)
        playlist.add(media_url, listitem)
        xbmc.Player().play(playlist)
        return

    if linkType == "DailyMotion":
        xbmcgui.Dialog().notification(__addonname__, "Playing " + linkType + " video", __icon__, 3000, False)
        playback_url = 'plugin://plugin.video.dailymotion_com/?url=%s&mode=playVideo' % video_id
        playlist.add(playback_url, listitem)
        xbmc.Player().play(playlist)

    if linkType == "Youtube":
        xbmcgui.Dialog().notification(__addonname__, "Playing " + linkType + " video", __icon__, 3000, False)
        playback_url = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % video_id
        playlist.add(playback_url, listitem)
        xbmc.Player().play(playlist)

    if linkType == "Facebook":
        import urlresolver
        xbmcgui.Dialog().notification(__addonname__, "Playing " + linkType + " video", __icon__, 3000, False)
        media_url = urlresolver.HostedMediaFile(host='facebook.com', media_id=video_id).resolve()
        playlist.add(media_url, listitem)
        xbmc.Player().play(playlist)

    if linkType == "Openload":
        import urlresolver
        xbmcgui.Dialog().notification(__addonname__, "Playing " + linkType + " video", __icon__, 3000, False)
        media_url = urlresolver.HostedMediaFile(host='openload.co', media_id=video_id).resolve()
        playlist.add(media_url, listitem)
        xbmc.Player().play(playlist)

    return


# Define function to monitor real time parameters ###
def get_params():
    param = []
    paramstring = sys.argv[2]
    print(sys.argv[2])
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if params[len(params) - 1] == '/':
            params = params[0:len(params) - 2]
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
    url = unquote_plus(params["url"])
except:
    pass
# noinspection PyBroadException
try:
    name = unquote_plus(params["name"])
except:
    pass
# noinspection PyBroadException
try:
    mode = int(params["mode"])
except:
    pass

try:
    provider = unquote_plus(params["provider"])
except:
    pass

print(params)
args = parse_qs(sys.argv[2][1:])
# noinspection PyRedeclaration
linkType = ''

# noinspection PyBroadException
try:
    linkType = args.get('linkType', '')[0]
except:
    pass

print(name, mode, url, linkType, provider)

with open(addonPath + '/runtime', 'r') as fout:
    script_time = float(fout.readline())
    if time.time() > (script_time + 1800):
        xbmc.executebuiltin('XBMC.RunScript(' + service_addon + ')')

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
    print('Something dint work')
    traceback.print_exc(file=sys.stdout)

if not (mode == 3):
    xbmcplugin.endOfDirectory(int(sys.argv[1]))