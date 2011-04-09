import json

from flask import g

from log import L

from processor import Processor

@Processor.processor
class DataLoader(Processor):

    def process(self):
        
        if self.token.request.method in ['PUT', 'POST' ]:
            self.token.data = json.loads(self.token.data)
            L.debug("DataLoader:: data=%r" % self.token.data)
