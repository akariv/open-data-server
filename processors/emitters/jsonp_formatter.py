import json

from base import Emitter

@Emitter.emitter
class JsonpFormatter(Emitter):
    
    def condition(self):
        format = self.token.get_request_format()
        self.callback = self.token.request.args.get('callback',None)
        return format == 'jsonp' and self.callback != None
    
    def format(self):
        self.token.content_type = 'text/javascript'
        self.token.response = "%s(%s);" % (self.callback, json.dumps(self.token.response))
