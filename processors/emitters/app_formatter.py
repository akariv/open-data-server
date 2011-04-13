import json

from base import Emitter
import urllib2

@Emitter.emitter
class AppFormatter(Emitter):
    
    APPS = { 'mks' : 'http://127.0.0.1:5000/' }
    
    def condition(self):
        format = self.token.get_request_format()
        if format != None:
            if format.startswith("app/"):
                self.app = format[4:]
                if self.app in self.APPS.keys():
                    return True
        return False
    
    def format(self):
        self.token.content_type = 'text/html'
        url = self.APPS.get(self.app)
        if self.token.slug != None:
            url += self.token.slug
        data = json.dumps(self.token.response)

        req = urllib2.Request(url,
                              headers = {
                                         "Content-Type": "application/json",
                                         "User-Agent": "open-data-server/1", # otherwise it uses "Python-urllib/..."
                                         },
                                data = data)
        self.token.response = urllib2.urlopen(req).read()