import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib2,urllib,cgi, re, urlresolver, os, traceback
import urlparse
import HTMLParser

Posturl="http://www.siasat.pk/forum/showthread.php?"
Nexturl="http://www.siasat.pk/forum/"
DTSurl="http://www.siasat.pk/forum/forumdisplay.php?29-Daily-Talk-Shows/"
DVurl="http://www.siasat.pk/forum/forumdisplay.php?21-Siasi-Videos"
SCurl="http://www.siasat.pk/forum/forumdisplay.php?37-Sports-Corner"


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


def addDir(name,url,mode,iconimage,showContext=False,isItFolder=True, linkType=None):
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


def AddEnteries(name, type=None):
	if type=='DTShows':
		AddShows(DTSurl)
	elif type=='DVideos':
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

	for urls, desc in zip(URL,Desc):
		addDir(desc, urls, 3, '', True, isItFolder=False)

	match =re.findall('<span class="prev_next"><a rel="next" href="(.*)["]\stitle="Next Page', link, re.IGNORECASE)

	if len(match)==2:
		addDir('Next Page' ,match[0] ,2,'',isItFolder=True)

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


print 	mode,url,linkType,name

try:
	if mode==None or url==None or len(url)<1:
		Addtypes()
	
	elif mode==2:
		AddEnteries(name, url)

	elif mode==3:
		print "Play url is "+url
		PlayShowLink(url)

except:
	print 'Something dint work'
	traceback.print_exc(file=sys.stdout)

if not (mode==3):
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
