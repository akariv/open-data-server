from flask import request, g

from processors import Processor
from tok import Token

PROCESSORS = [ "DataLoader",
#               "PermissionChecker",
               "CacheGetter",
               "DBOperation",
               "MultiLang",
               "ReferenceFetcher",
               "CacheSetter",
               "DataFormatter" ]

def process(path,slug):
    token = Token(request,path,slug,g.user)
    
    to_skip = None
    for name in PROCESSORS:
        if to_skip != None:
            if name == to_skip:
                to_skip = None
            else:
                continue
        P = Processor.get_processor(name)
        processor = P(token) 
        processor.process()
        if processor.stop():
            to_skip = processor.skip()
    
    return token.response, token.content_type, token.headers
