from flask import request

from processors import Processor
from tok import Token

PROCESSORS = [ "DataLoader",
               "DBOperation",
               "MultiLang",
               "ReferenceFetcher",
               "DataFormatter" ]

def process(path,slug):
    token = Token(request,path,slug)
    
    for name in PROCESSORS:
        P = Processor.get_processor(name)
        P(token).process()
    
    return token.response, token.content_type, token.headers
