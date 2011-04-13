from flask import abort

from processor import Processor
from processors.emitters import Emitter

from log import L

EMITTERS = [ "AppFormatter",
             "CsvFormatter",
             "ExcelFormatter",
             "HtmlFormatter",
             "JsonpFormatter",
             "JsonFormatter"]

@Processor.processor
class DataFormatter(Processor):

    def process(self):
        
        for emitter in EMITTERS:
            E = Emitter.get_emitter(emitter)
            e = E(self.token)
            if e.condition():
                L.debug("DataFormatter:: using emitter %s" % emitter)
                e.format()
                L.debug("DataFormatter:: token.response=%r (%s)" % (self.token.response,self.token.content_type))
                return
        abort(400)