import json

from flask import g

from log import L

from processor import Processor

@Processor.processor
class DataLoader(Processor):

    def process(self):
        
        if self.token.request.method in ['PUT', 'POST' ]:
            try:
                self.token.data = json.loads(self.token.data)
            except:
                self.token.data = dict( [ (k,v) for k,v in self.token.request.form.iteritems() ] )
            L.debug("DataLoader:: data=%r" % self.token.data)
