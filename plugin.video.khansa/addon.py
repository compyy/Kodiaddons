#Youtubeurl:plugin://plugin.video.youtube/play/?video_id=id
#Dailymotionurl:plugin://plugin.video.dailymotion/?url=id&mode=playVideo

import os, xbmc

videoList = xbmc.PlayList(xbmc.PLAYLIST_VIDEO)
videoList.clear()

path = os.getcwd()+"/addons/plugin.video.khansa/"

videoList.load((path+"playlist.m3u"))

# shuffle playlist
videoList.shuffle()

# put playlist on repeat
xbmc.executebuiltin("xbmc.playercontrol(RepeatAll)")

# play playlist
xbmc.Player().play(videoList)
