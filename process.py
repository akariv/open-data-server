from flask import request

from processors import Processor
from tok import Token

PROCESSORS = [ "DataLoader",
               "PermissionChecker",
               "DBOperation",
               "MultiLang",
               "ReferenceFetcher",
               "DataFormatter" ]

def process(path,slug):
    token = Token(request,path,slug)
    
    for name in PROCESSORS:
        P = Processor.get_processor(name)
        processor = P(token) 
        processor.process()
        if processor.stop():
            break
    
    return token.response, token.content_type, token.headers
