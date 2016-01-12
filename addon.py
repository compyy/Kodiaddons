import xbmc, xbmcgui, xbmcplugin
import urllib2,urllib,cgi, re, urlresolver  
import urlparse
import HTMLParser
import xbmcaddon
from operator import itemgetter
import traceback,cookielib
import base64,os,  binascii
from time import time


class NoRedirection(urllib2.HTTPErrorProcessor):
   def http_response(self, request, response):
       return response
   https_response = http_response

def ShowSettings(Fromurl):
	selfAddon.openSettings()

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
				
	return param


	
def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok


def addDir(name,url,mode,iconimage,showContext=False,showLiveContext=False,isItFolder=True, linkType=None):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )

	if showContext==True:
		cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "DM")
		cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "LINK")
		cmd3 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "Youtube")
		cmd4 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "PLAYWIRE")
		cmd5 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "EBOUND")
		cmd6 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "PLAYWIRE")
		cmd7 = "XBMC.RunPlugin(%s&linkType=%s)" % (u, "VIDRAIL")
		
		liz.addContextMenuItems([('Show All Sources',cmd6),('Play Vidrail video',cmd7),('Play Ebound video',cmd5),('Play Playwire video',cmd4),('Play Youtube video',cmd3),('Play DailyMotion video',cmd1),('Play Tune.pk video',cmd2)])
	if linkType:
		u="XBMC.RunPlugin(%s&linkType=%s)" % (u, linkType)

	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isItFolder)
	return ok

def Addtypes():
	addDir('Daily Talk Shows' ,'DTShows' ,2,'')
	addDir('Daily Vidoes' ,'DVidoes' ,2,'')
	addDir('Sports Corner' ,'SCorner' ,2,'')

def AddEnteries(name, type=None):
    if type=='DTShows':
        AddShows(mainurl)
    elif type=='DVideos':
        AddDVideos(mainurl)
    elif type=='SCorner':
        AddSCorner(mainurl)
    elif name=='Next Page' or mode==43:
        AddShows(url)

    return

def getUrl(url, cookieJar=None,post=None, timeout=20, headers=None):
    cookie_handler = urllib2.HTTPCookieProcessor(cookieJar)
    opener = urllib2.build_opener(cookie_handler, urllib2.HTTPBasicAuthHandler(), urllib2.HTTPHandler())
    req = urllib2.Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36')
    if headers:
        for h,hv in headers:
            req.add_header(h,hv)

    response = opener.open(req,post,timeout=timeout)
    link=response.read()
    response.close()
    return link;

def AddShows(Fromurl):
    headers=[('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
    try:
        linkfull=getUrl(Fromurl,cookieJar=CookieJar, headers=headers)
    except:
        import cloudflare
        cloudflare.createCookie(Fromurl,CookieJar,'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        linkfull=getUrl(Fromurl,cookieJar=CookieJar, headers=headers)


    CookieJar.save (ZEMCOOKIEFILE,ignore_discard=True)

    link=linkfull
    if '<div id="top-articles">' in linkfull:
        link=linkfull.split('<div id="top-articles">')[0]
        
    match =re.findall('<div class="thumbnail">\\s*<a href="(.*?)".*\s*<img class="thumb".*?src="(.*?)" alt="(.*?)"', link, re.UNICODE)
    if len(match)==0:
        match =re.findall('<div class="thumbnail">\s*<a href="(.*?)".*\s*<img.*?.*?src="(.*?)".* alt="(.*?)"', link, re.UNICODE)

    if not '/page/' in Fromurl:
        try:
            pat='\\<a href="(.*?)".*>\\s*<img.*?src="(.*?)".*\\s?.*?\\s*?<h1.*?>(.*?)<'
            matchbanner=re.findall(pat, linkfull, re.UNICODE)
            if len(matchbanner)>0:
                match=matchbanner+match
        except: pass

        
    h = HTMLParser.HTMLParser()

    
    for cname in match:
        tname=cname[2]
        tname=re.sub(r'[\x80-\xFF]+', convert,tname )
        addDir(tname,cname[0] ,3,cname[1], True,isItFolder=False)
        

    match =re.findall('<a class="nextpostslink" rel="next" href="(.*?)">', link, re.IGNORECASE)

    if len(match)==1:
        addDir('Next Page' ,match[0] ,2,'',isItFolder=True)

    return

def ShowAllSources(url, loadedLink=None):
	global linkType
	link=loadedLink
	if not loadedLink:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
	available_source=[]
	playURL =re.findall('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"', link)

	if not len(playURL)==0:
		available_source.append('Playwire Source')

	playURL =re.findall('data-config="(.*?config.playwire.com.*?)"', link)

	if not len(playURL)==0:
		available_source.append('Playwire Source')

	playURL =re.findall('src="(.*?ebound\\.tv.*?)"', link)

	if not len(playURL)==0:
		available_source.append('Ebound Source')		
	else:
		playURL =re.findall('src="(.*?poovee\.net.*?)"', link)
		if not len(playURL)==0:
			available_source.append('Ebound Source')		
        
	playURL= match =re.findall('src="(.*?(dailymotion).*?)"',link)
	if not len(playURL)==0:
		available_source.append('Daily Motion Source')

	playURL= match =re.findall('src="(.*?(vidrail\.com).*?)"',link)
	if not len(playURL)==0:
		available_source.append('Vidrail Source')
        
	playURL= match =re.findall('src="(.*?(tune\.pk).*?)"', link)
	if not len(playURL)==0:
		available_source.append('Link Source')

	playURL= match =re.findall('<strong>Youtube<\/strong>.*?src=\".*?embed\/(.*?)\?.*\".*?<\/iframe>', link,re.DOTALL| re.IGNORECASE)
	if not len(playURL)==0:
		available_source.append('Youtube Source')

	if len(available_source)>0:
		dialog = xbmcgui.Dialog()
		index = dialog.select('Choose your stream', available_source)
		if index > -1:
			linkType=available_source[index].replace(' Source','').replace('Daily Motion','DM').upper()
			PlayShowLink(url);

def PlayShowLink ( url ): 
    global linkType
    headers=[('User-Agent','Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')]
    CookieJar=getZemCookieJar()
    link=getUrl(url,cookieJar=CookieJar, headers=headers)
    line1 = "Playing DM Link"
    time = 5000  #in miliseconds
    defaultLinkType=0 #0 youtube,1 DM,2 tunepk
    defaultLinkType=selfAddon.getSetting( "DefaultVideoType" ) 
    print "LT link is" + linkType
    if linkType.upper()=="SHOWALL" or (linkType.upper()=="" and defaultLinkType=="4"):
        ShowAllSources(url,link)
        return
    if linkType.upper()=="DM" or (linkType=="" and defaultLinkType=="0"):
        line1 = "Playing DM Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1,time  , __icon__))
        playURL= match =re.findall('src="(http.*?(dailymotion.com).*?)"',link)
        if len(playURL)==0:
            line1 = "Daily motion link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return 
        playURL=match[0][0]
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        stream_url = urlresolver.HostedMediaFile(playURL).resolve()
        print stream_url
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
    elif  linkType.upper()=="EBOUND"  or (linkType=="" and defaultLinkType=="3"):
        line1 = "Playing Ebound Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
        playURL= match =re.findall(' src=".*?ebound\\.tv.*?site=(.*?)&.*?date=(.*?)\\&', link)
        if len(playURL)>0:
            playURL=match[0]
            dt=playURL[1]
            clip=playURL[0]
            urli=base64.b64decode('aHR0cDovL3d3dy5lYm91bmRzZXJ2aWNlcy5jb20vaWZyYW1lL25ldy92b2RfdWdjLnBocD9zdHJlYW09bXA0OnZvZC8lcy8lcyZ3aWR0aD02MjAmaGVpZ2h0PTM1MCZjbGlwPSVzJmRheT0lcyZtb250aD11bmRlZmluZWQ=')%(dt,clip,clip,dt)
            post = {'username':'hash'}
            post = urllib.urlencode(post)
            req = urllib2.Request(base64.b64decode('aHR0cDovL2Vib3VuZHNlcnZpY2VzLmNvbS9mbGFzaHBsYXllcmhhc2gvaW5kZXgucGhw'))
            req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.117 Safari/537.36')
            response = urllib2.urlopen(req,post)
            link=response.read()
            response.close()
            strval =link;# match[0]
            stream_url=base64.b64decode('cnRtcDovL2Nkbi5lYm91bmQudHYvdm9kIHBsYXlwYXRoPW1wNDp2b2QvJXMvJXMgYXBwPXZvZD93bXNBdXRoU2lnbj0lcyBzd2Z1cmw9aHR0cDovL3d3dy5lYm91bmRzZXJ2aWNlcy5jb20vbGl2ZS92Ni9wbGF5ZXIuc3dmP2RvbWFpbj13d3cuemVtdHYuY29tJmNoYW5uZWw9JXMmY291bnRyeT1FVSBwYWdlVXJsPSVzIHRjVXJsPXJ0bXA6Ly9jZG4uZWJvdW5kLnR2L3ZvZD93bXNBdXRoU2lnbj0lcyBsaXZlPXRydWUgdGltZW91dD0xNQ==')%(dt,clip,strval,clip,urli,strval)
        else:
            playURL=match=re.findall('src="(.*?(poovee\.net).*?)"', link)
            
            if len(playURL)==0:
                line1 = "EBound/Povee link not found"
                xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
                ShowAllSources(url,link)
                return 
            playURL=match[0][0]
            pat='<source src="(.*?)"'
            link=getUrl(playURL,cookieJar=CookieJar, headers=headers)
            playURL=re.findall(pat, link)
            stream_url=playURL[0]
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
    elif  linkType.upper()=="VIDRAIL"  or (linkType=="" and defaultLinkType=="5"):
        line1 = "Playing Vidrail Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
        playURL= match =re.findall('src="(.*?(vidrail\.com).*?)"', link)
        if len(playURL)==0:
            line1 = "Vidrail link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return 

        playURL=match[0][0]
        pat='<source src="(.*?)"'
        link=getUrl(playURL,cookieJar=CookieJar, headers=headers)
        playURL=re.findall(pat, link)
        if len(playURL)==0:
            line1 = "Vidrail link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return 
        stream_url=playURL[0]
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')

        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
    elif  linkType.upper()=="LINK"  or (linkType=="" and defaultLinkType=="1"):
        line1 = "Playing Tune.pk Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))

        playURL= match =re.findall('src="(.*?(tune\.pk).*?)"', link)
        if len(playURL)==0:
            line1 = "Link.pk link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return 

        playURL=match[0][0]
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        stream_url = urlresolver.HostedMediaFile(playURL).resolve()
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)
    elif  linkType.upper()=="PLAYWIRE"  or (linkType=="" and defaultLinkType=="2"):
        line1 = "Playing Playwire Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
        playURL =re.findall('src=".*?(playwire).*?data-publisher-id="(.*?)"\s*data-video-id="(.*?)"', link)
        V=1
        if len(playURL)==0:
            playURL =re.findall('data-config="(.*?config.playwire.com.*?)"', link)
            V=2
        if len(playURL)==0:
            line1 = "Playwire link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return 
        if V==1:
            (playWireVar,PubId,videoID)=playURL[0]
            cdnUrl=base64.b64decode("aHR0cDovL2Nkbi5wbGF5d2lyZS5jb20vdjIvJXMvY29uZmlnLyVzLmpzb24=")%(PubId,videoID)
            req = urllib2.Request(cdnUrl)
            req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
            response = urllib2.urlopen(req)
            link=response.read()
            response.close()
            playURL =base64.b64decode("aHR0cDovL2Nkbi5wbGF5d2lyZS5jb20vJXMvJXM=")%(PubId,re.findall('src":".*?mp4:(.*?)"', link)[0])

        else:
            playURL=playURL[0]
            if playURL.startswith('//'): playURL='http:'+playURL

            reg='media":\{"(.*?)":"(.*?)"'
            req = urllib2.Request(playURL)
            req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
            response = urllib2.urlopen(req)
            link=response.read()
            playURL =re.findall(reg, link)
            if len(playURL)>0:
                playURL=playURL[0]
                ty=playURL[0]
                innerUrl=playURL[1]

                req = urllib2.Request(innerUrl)
                req.add_header('User-Agent', 'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
                response = urllib2.urlopen(req)
                link=response.read()
                reg='baseURL>(.*?)<\/baseURL>\s*?<media url="(.*?)"'
                playURL =re.findall(reg, link)[0]
                playURL=playURL[0]+'/'+playURL[1]
        playlist = xbmc.PlayList(1)
        playlist.clear()
        listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
        listitem.setInfo("Video", {"Title":name})
        listitem.setProperty('mimetype', 'video/x-msvideo')
        listitem.setProperty('IsPlayable', 'true')
        stream_url = playURL
        playlist.add(stream_url,listitem)
        xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
        xbmcPlayer.play(playlist)

    else:
        line1 = "Playing Youtube Link"
        xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
        youtubecode= match =re.findall('<strong>Youtube<\/strong>.*?src=\".*?embed\/(.*?)\?.*\".*?<\/iframe>', link,re.DOTALL| re.IGNORECASE)
        if len(youtubecode)==0:
            line1 = "Youtube link not found"
            xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(__addonname__,line1, time, __icon__))
            ShowAllSources(url,link)
            return
        youtubecode=youtubecode[0]
        uurl = 'plugin://plugin.video.youtube/?action=play_video&videoid=%s' % youtubecode
        xbmc.executebuiltin("xbmc.PlayMedia("+uurl+")")

    return


params=get_params()
url=None
name=None
mode=None
linkType=None

try:
	url=urllib.unquote_plus(params["url"])
except:
	pass
try:
	name=urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode=int(params["mode"])
except:
	pass


args = cgi.parse_qs(sys.argv[2][1:])
linkType=''
try:
	linkType=args.get('linkType', '')[0]
except:
	pass


print 	mode,url,linkType

try:
	if mode==None or url==None or len(url)<1:
		print "InAddTypes"
		Addtypes()
	elif mode==2 or mode==43:
		print "Ent url is ",name,url        
		AddEnteries(name, url)
        
except:
	print 'somethingwrong'
	traceback.print_exc(file=sys.stdout)
	

if not ((mode==2)):
	if mode==144:
		xbmcplugin.endOfDirectory(int(sys.argv[1]),updateListing=True)
	else:
		xbmcplugin.endOfDirectory(int(sys.argv[1]))
