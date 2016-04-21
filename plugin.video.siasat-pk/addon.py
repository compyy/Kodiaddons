import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib2,urllib, re, os, traceback, cgi
import requests



Posturl="http://www.siasat.pk/forum/showthread.php?"
Nexturl="http://www.siasat.pk/forum/"
DTSurl="http://www.siasat.pk/forum/forumdisplay.php?29-Daily-Talk-Shows/"
DVurl="http://www.siasat.pk/forum/forumdisplay.php?21-Siasi-Videos/"
SCurl="http://www.siasat.pk/forum/forumdisplay.php?37-Sports-Corner/"
Auto_Play=True

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

	return


def addDir(name,url,mode,iconimage,isItFolder=True,Context=False):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True

	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	
	if Context==True:
		cmd1="DailyMotion Link not Available"
		cmd2="Youtube Link not Available"
		cmd1 = "PlayShowLink(%s,%s)" % ("DailyMotion",url)
		cmd2 = "PlayShowLink(%s,%s)" % ("Youtube",url)
		liz.addContextMenuItems([("Play DailyMotion",cmd1),("Play Youtube",cmd2)])
		

	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=isItFolder)
	return ok


def AddEnteries(name, type=None):
	if type=='DTShows':
		AddShows(DTSurl)
	elif type=='DVidoes':
		AddShows(DVurl)
	elif type=='SCorner':
		AddShows(SCurl)
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
		addDir(desc, urls, 3, img, True)

	match =re.findall('<span class="prev_next"><a rel="next" href="(.*)["]\stitle="Next Page', link, re.IGNORECASE)

	if len(match)==2:
		addDir('Next Page' ,match[0] ,2,'', True)

	return

def convert(s):
    try:
        return s.group(0).encode('latin1').decode('utf8')
    except:
        return s.group(0)

def GetShowLink(url):
	headers = {'User-Agent' : 'Mozilla 5.10'}
	request=urllib2.Request(url, None, headers)
	response=urllib2.urlopen(request)
	link=response.read()
	did=re.findall('<iframe.*src=["]http.*dailymotion.com.*video[/](.*)[?].*["]',link)
	yid=re.findall('<iframe.*YouTube.*src=["].*youtube[.]com.*[/](.*)[?].*["].*iframe>',link)

	if did:
		#addDir("DailyMotion", did[0], 4, '', isItFolder=False)
		PlayShowLink("DailyMotion", did[0])
		
	
	elif yid:
		#addDir("Youtube", yid[0], 4, '', isItFolder=False)
		PlayShowLink("Youtube", yid[0])

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


print 	mode,url,name

try:
	if mode==None or url==None or len(url)<1:
		Addtypes()
	
	elif mode==2:		
		AddEnteries(name, url)

	elif mode==3:
		GetShowLink(Posturl+url)

	#elif mode==4:
		#PlayShowLink(name,url)

except:
	print 'Something dint work'
	traceback.print_exc(file=sys.stdout)

if not (mode==3):
	xbmcplugin.endOfDirectory(int(sys.argv[1]))