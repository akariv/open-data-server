import json

from flask import g

from log import L

from processor import Processor
from internal_db_ops import internal_find

@Processor.processor
class ReferenceFetcher(Processor):

    def handle_object(self,obj):
        
        if type(obj) == dict and len(obj.keys())==1 and obj.has_key('_ref'):
            
            L.info("ReferenceFetcher: Attempting to fetch %r" % obj)
            
            url = obj['_ref']
            if url.strip() == '':
                return None
            
            data = None
            try:
                data = internal_find(url,obj,follow=False,lang=self.token.lang)
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
