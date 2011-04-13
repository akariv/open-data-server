import json

from flask import g

from log import L

from processor import Processor

@Processor.processor
class ReferenceFetcher(Processor):

    def handle_object(self,obj):
        
        if type(obj) == dict and len(obj.keys())==1 and obj.has_key('_ref'):
            
            url = obj['_ref']
            data = None
            try:
                url = '/' + url
                data = g.app.test_client().get(url).data
                data = json.loads(data)
                if data != None:
                    return data
            except:
                pass
            
        elif type(obj) == dict:
            return dict([ (k,self.handle_object(v)) for k,v in obj.iteritems()])

        elif type(obj) == list:
            return [ self.handle_object(el) for el in obj]
        
        return obj

    def process(self):
        
        if self.token.request.args.get('follow','yes') == 'no':
            return
        self.token.response = self.handle_object(self.token.response)
