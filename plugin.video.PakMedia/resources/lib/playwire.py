import urllib2
import re

def resolve(playURL):
    if playURL.startswith('//'):
        playURL = 'http:' + playURL
        print playURL

    reg = 'media":\{"(.*?)":"(.*?)"'
    req = urllib2.Request(playURL)
    req.add_header('User-Agent',
                   'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
    response = urllib2.urlopen(req)
    link = response.read()
    playURL = re.findall(reg, link)
    if len(playURL) > 0:
        playURL = playURL[0]
        innerUrl = playURL[1]
        print innerUrl
        req = urllib2.Request(innerUrl)
        req.add_header('User-Agent',
                       'Mozilla/5.0(iPad; U; CPU iPhone OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B314 Safari/531.21.10')
        response = urllib2.urlopen(req)
        link = response.read()
        reg = 'baseURL>(.*?)<\/baseURL>\s*?<media url="(.*?)"'
        playURL = re.findall(reg, link)[0]
        playURL = playURL[0] + '/' + playURL[1]
        return playURL

    return None