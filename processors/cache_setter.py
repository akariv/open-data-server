import json

from flask import g

from log import L

from processor import Processor
from processors.cache_checker import store_in_cache

@Processor.processor
class CacheSetter(Processor):
    
    def process(self):
        data = json.dumps(self.token.response)
        if self.token.request.method == "GET":
            if data != 'null':
                L.info("CacheSetter: storing in %s <== %s" % (self.token.cache_key,str(data)[:2048]))
                store_in_cache(self.token.cache_key,data)
                
