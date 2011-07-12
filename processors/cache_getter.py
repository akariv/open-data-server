import json

from flask import g

from log import L, snip

from processor import Processor
from processors.cache_checker import hit_cache, clear_cache,\
    clear_cache_for_path

@Processor.processor
class CacheGetter(Processor):

    ARGS_FOR_KEY = [ 'lang', 'follow',
                     'query', 'order', 'start', 'limit', 'fields',
                     'count' ]
    
    def process(self):
        self.token.cache_key = json.dumps(self.token.path) + '|' + json.dumps(self.token.slug) + '|' + '|'.join([ self.token.request.args.get(arg,'') for arg in self.ARGS_FOR_KEY ])
        if self.token.request.args.get('hitcache',"1") == "0":
            L.info("Skipping cache as requested for %s/%s" % (self.token.path,self.token.slug))
            return 
        if self.token.request.method == "GET":
            data = hit_cache(self.token.cache_key)
            L.info("Data for key %s == %s" % (self.token.cache_key,snip(repr(data))))
            if data != None:
                self.token.response = json.loads(data)
                self.should_stop = True
                self.skip_to = "DataFormatter"
        else:
            clear_cache(self.token.cache_key)
            clear_cache_for_path(self.token.path)
