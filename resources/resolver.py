import re
import xbmc
import urllib
import urllib2
import xbmcgui
from time import sleep

class StreamcloudResolver:
    canceled = False
   
    def get_mirror_url(self, title, mirror, season, episode):
        url = "http://kinox.to/aGET/Mirror/%s&Hoster=30&Mirror=%s" % \
            (title, mirror)
            
        if season and episode:
            url += '&Season=%s&Episode=%s' % (season, episode)
        return url

    def get_media_url(self, web_url):    
        try:
            req = urllib2.Request(web_url)
            response = urllib2.urlopen(req)
            content = response.read()
        
            if not re.search('id=\"btn_download\"', content):
                raise Exception ('File Not Found or removed')
            
            #show dialog with progress bar
            pDialog = xbmcgui.DialogProgress()
            pDialog.create('XBMC', 'Initializing video...')
        
            form_values = {}
            for i in re.finditer(
                    '<input.*?name="(.*?)".*?value="(.*?)">', content):
                form_values[i.group(1)] = i.group(2)
                        
            #wait 11 seconds and update progress bar            
            for x in range(11):
                pDialog.update(int((x/10.0) * 100))
                xbmc.sleep(1000)
                
                if pDialog.iscanceled():
                    self.canceled = True
                    return
            
            content = urllib2.urlopen(
                url=web_url, 
                data=urllib.urlencode(form_values)
            ).read()
                
            r = re.search('file: "(.+?)",', content)
            
            pDialog.close()
            
            if r:
                return r.group(1)
            else:
                raise Exception ('File Not Found or removed')

        except Exception, e:
            print 'Streamcloud Error occured: %s' % e