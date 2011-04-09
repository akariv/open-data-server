import json

from base import Emitter

@Emitter.emitter
class JsonFormatter(Emitter):
    
    def condition(self):
        format = self.token.get_request_format()
        return format == 'json' or format == None
    
    def format(self):
        self.token.content_type = 'application/json'
        self.token.response = json.dumps(self.token.response)
