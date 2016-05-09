import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib2,urllib, re, os, traceback, cgi
import requests

Posturl="http://www.siasat.pk/forum/showthread.php?"
Nexturl="http://www.siasat.pk/forum/"
DTSurl="http://www.siasat.pk/forum/forumdisplay.php?29-Daily-Talk-Shows/"
DVurl="http://www.siasat.pk/forum/forumdisplay.php?21-Siasi-Videos/"
SCurl="http://www.siasat.pk/forum/forumdisplay.php?37-Sports-Corner/"
Islurl="http://www.siasat.pk/forum/forumdisplay.php?30-Islamic-Corner"
STurl="http://www.siasat.pk/forum/forumdisplay.php?39-Science-and-Technology"
Hlurl="http://www.siasat.pk/forum/forumdisplay.php?42-Health-amp-Medical"



__addon__       = xbmcaddon.Addon()
__addonname__   = __addon__.getAddonInfo('name')
__icon__        = __addon__.getAddonInfo('icon')
addon_id = 'plugin.video.siasat-pk'
selfAddon = xbmcaddon.Addon(id=addon_id)
profile_path =  xbmc.translatePath(selfAddon.getAddonInfo('profile'))

addonPath = xbmcaddon.Addon().getAddonInfo("path")
addonversion =xbmcaddon.Addon().getAddonInfo("version")

if not selfAddon.getSetting( "dummy" )=="true":
    selfAddon.setSetting( "dummy" ,"true")
	
def ShowSettings(Fromurl):
	selfAddon.openSettings()

def get_params():
	param=[]
	paramstring=sys.argv[2]
	print sys.argv[2]
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


def Addtypes():
	addDir('Daily Talk Shows' ,'DTShows' ,2,'')
	addDir('Daily Vidoes' ,'DVidoes' ,2,'')
	addDir('Sports Corner' ,'SCorner' ,2,'')
	addDir('Science and Technology' ,'SCTC' ,2,'')
	addDir('Islamic Videos' ,'Isl' ,2,'')
	addDir('Health and Medical' ,'Hlmd' ,2,'')
	addDir('Settings' ,'Settings' ,99,'',isItFolder=False)

	return


def addDir(name,url,mode,iconimage,showContext=False,isItFolder=True,linkType=None):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	if showContext==True:
		cmd1 = "XBMC.RunPlugin(%s&linkType=%s)" % (u,"DailyMotion")
		cmd2 = "XBMC.RunPlugin(%s&linkType=%s)" % (u,"Youtube")
		liz.addContextMenuItems([('Play DailyMotion video',cmd1),('Play Youtube video',cmd2)],replaceItems=True)
	
	if linkType:
		u="XBMC.RunPlugin(%s&linkType=%s)" % (u, linkType)
		
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isItFolder)
	return ok

def AddEnteries(name, type=None):
	if type=='DTShows':
		AddShows(DTSurl)
	elif type=='DVidoes':
		AddShows(DVurl)
	elif type=='SCorner':
		AddShows(SCurl)
	elif type=='SCTC':
		AddShows(STurl)
	elif type=='Isl':
		AddShows(Islurl)
	elif type=='Hlmd':
		AddShows(Hlurl)
	elif name=='Next Page':
		AddShows((Nexturl+url))

	return

def AddShows(Fromurl):
	headers = {'User-Agent' : 'Mozilla 5.10'}
	request=urllib2.Request(Fromurl, None, headers)
	response=urllib2.urlopen(request)
	link=response.read()
	
	URL = re.compile('[<]a style.*id[=]["]thread_title_(.*)["][>]', re.IGNORECASE).findall(link)
	Desc = re.compile('[<]a style.*["]\sid[=]["]thread.*["]>(.*)[<]').findall(link)
	IMG_list = re.compile('[<]img src[=]["](.*)["]\sstyle.*[>]').findall(link)
	IMG = []
	
	for i in IMG_list:
		IMG.append(re.sub("amp;", "",i))
		
	for urls, desc, img in zip(URL,Desc,IMG):
		addDir(desc, urls, 3, img, showContext=True, isItFolder=True)

	match =re.findall('<span class="prev_next"><a rel="next" href="(.*)["]\stitle="Next Page', link, re.IGNORECASE)

	if len(match)==2:
		addDir('Next Page' ,match[0] ,2,'', isItFolder=True)

	return

def convert(s):
    try:
        return s.group(0).encode('latin1').decode('utf8')
    except:
        return s.group(0)

def GetShowLink(url):
	global linkType
	headers = {'User-Agent' : 'Mozilla 5.10'}
	request=urllib2.Request(url, None, headers)
	response=urllib2.urlopen(request)
	link=response.read()
	available_source=[]
	available_link=[]
	Auto_Play=selfAddon.getSetting("APlay")
	defaultLinkType=0 #0 DailyMotion, #1 Youtube
	defaultLinkType=selfAddon.getSetting("DefaultVideoType")
	
	did=re.findall('<iframe.*src=["]http.*dailymotion.com.*video[/](.*)[?].*["]',link)
	if did:
		available_source.append("DailyMotion")
		available_link.append(did[0])
		
	yid=re.findall('<iframe.*YouTube.*src=["].*youtube[.]com.*[/](.*)[?].*["].*iframe>',link)
	if yid:
		available_source.append("Youtube")
		available_link.append(yid[0])
	
	if len(available_source)>0:
		if Auto_Play=="true":
			if defaultLinkType=="0":
				for i in available_source:
					if	i=="DailyMotion":
						PlayShowLink(i, did[0])
						return
				
			if defaultLinkType=="1":
				for i in available_source:
					if i=="Youtube":
						PlayShowLink(i, yid[0])
						return
			
			xbmcgui.Dialog().ok(__addonname__,"No Valid Link Available for Default Play Source")
				
		dialog = xbmcgui.Dialog()
		index = dialog.select('Choose your stream', available_source)
		
		if index > -1:
			linkType=available_source[index]
			linkurl=available_link[index]
		
		
		if linkType:
				PlayShowLink(linkType, linkurl)
				
			
	else:
		xbmcgui.Dialog().ok(__addonname__,"No Valid link found in the post")
	
	return


def PlayShowLink(name,url):
	if name=="DailyMotion":
		xbmc.executebuiltin('PlayMedia(plugin://plugin.video.dailymotion/?url='+url+'&mode=playVideo)')

	if name=="Youtube":
		xbmc.executebuiltin('PlayMedia(plugin://plugin.video.youtube/play/?video_id='+url+')')
	
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


print 	mode,url,name,linkType

try:
	if mode==None or url==None or len(url)<1:
		Addtypes()
	
	elif mode==2:		
		AddEnteries(name, url)

	elif mode==3:
		GetShowLink(Posturl+url)

	elif mode==99 :
		ShowSettings(url)

except:
	print 'Something dint work'
	traceback.print_exc(file=sys.stdout)

if not (mode==3):
	xbmcplugin.endOfDirectory(int(sys.argv[1]))