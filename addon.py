import xbmc, xbmcgui, xbmcplugin, xbmcaddon
import urllib2,urllib, re, urlresolver, os, traceback, cgi
import requests

pluginhandle = int(sys.argv[1])

Posturl="http://www.siasat.pk/forum/showthread.php?"
Nexturl="http://www.siasat.pk/forum/"
DTSurl="http://www.siasat.pk/forum/forumdisplay.php?29-Daily-Talk-Shows/"
DVurl="http://www.siasat.pk/forum/forumdisplay.php?21-Siasi-Videos/"
SCurl="http://www.siasat.pk/forum/forumdisplay.php?37-Sports-Corner/"


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

	for urls, desc in zip(URL,Desc):
		addDir(desc, urls, 3, '', True, isItFolder=True)

	match =re.findall('<span class="prev_next"><a rel="next" href="(.*)["]\stitle="Next Page', link, re.IGNORECASE)

	if len(match)==2:
		addDir('Next Page' ,match[0] ,2,'',isItFolder=True)

	return

def PlayShowLink(url):
	headers = {'User-Agent' : 'Mozilla 5.10'}
	request=urllib2.Request(url, None, headers)
	response=urllib2.urlopen(request)
	link=response.read()
	id=match=re.findall('<iframe.*src=["]http.*dailymotion.com.*video[/](.*)[?].*["]',link)
	playVideo(id[0])

	return

def playVideo(id):
	url = getStreamUrl(id)
	print url
	if url and not '.f4mTester' in url:
		playlist = xbmc.PlayList(1)
		playlist.clear()
		listitem = xbmcgui.ListItem(name, iconImage="DefaultVideo.png")
		listitem.setInfo("Video", {"Title":name})
		listitem.setProperty('mimetype', 'video/x-msvideo')
		listitem.setProperty('IsPlayable', 'true')
		playlist.add(url,listitem)
	
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(playlist)
			
		#listitem = xbmcgui.ListItem(path=url)
		#xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)

	elif url:
		xbmc.executebuiltin('XBMC.RunPlugin('+url+')')
	
	else:
		print 'No playable url found'


def getStreamUrl(id, live=False):
    print 'The url is ::',id
    headers = {'User-Agent':'Android'}
    cookie = {'Cookie':"lang=\"en_EN\"; family_filter=off"}
    r = requests.get("http://www.dailymotion.com/player/metadata/video/"+id,headers=headers,cookies=cookie)
    content = r.json()
    if content.get('error') is not None:
        Error = 'DailyMotion Says:[COLOR yellow]%s[/COLOR]' %(content['error']['title'])
        xbmc.executebuiltin('XBMC.Notification(Info:,'+ Error +' ,5000)')
        return
    else:

        cc= content['qualities']  #['380'][0]['url']
           
        m_url = ''
        other_playable_url = []
        for source,auto in cc.items():
            print source 
            for m3u8 in auto:
                m_url = m3u8.get('url',None)
                if m_url:
                    if not live:
                        if  source == '1080':
                            return m_url        
                
                        elif source == '720': #720 found no more iteration need
                            return m_url
                        elif source == '480': #send cookie for mp4
                            return m_url+'|Cookie='+r.headers['set-cookie']
                        elif source == '380': #720 found no more iteration need
                            return m_url+'|Cookie='+r.headers['set-cookie']
                        elif source == '240': #720 found no more iteration need
                            return m_url+'|Cookie='+r.headers['set-cookie']
                         
                        elif '.mnft' in m_url:
                            continue
                         
                    else:
                        if '.m3u8?auth' in m_url:
                            m_url = m_url.split('?auth=')
                            the_url = m_url[0] + '?redirect=0&auth=' + urllib.quote(m_url[1])
                            rr = requests.get(the_url,cookies=r.cookies.get_dict() ,headers=headers)
                            if rr.headers.get('set-cookie'):
                                print 'adding cookie to url'
                                return rr.text.split('#cell')[0]+'|Cookie='+rr.headers['set-cookie']
                            else:
                                return rr.text.split('#cell')[0]
                    other_playable_url.append(m_url) 
        if len(other_playable_url) >0: # probable not needed only for last resort
            for m_url in other_playable_url:
                if '.m3u8?auth' in m_url:
                    sep_url = m_url.split('?auth=')
                    the_url = sep_url[0] + '?redirect=0&auth=' + urllib.quote(sep_url[1])
                    rr = requests.get(the_url,cookies=r.cookies.get_dict() ,headers=headers)
                    if rr.headers.get('set-cookie'):
                        print 'adding cookie to url'
                        return rr.text.split('#cell')[0]+'|Cookie='+rr.headers['set-cookie']
                    else:
                        return rr.text.split('#cell')[0]



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
		PlayShowLink(Posturl+url)

except:
	print 'Something dint work'
	traceback.print_exc(file=sys.stdout)

if not (mode==3):
	xbmcplugin.endOfDirectory(int(sys.argv[1]))
