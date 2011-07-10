from flask import abort

from processor import Processor
from processors.emitters import Emitter

from log import L, snip

EMITTERS = [
             "TemplatePFormatter",
             "TemplateFormatter",
             "StaticFileFormatter",
             "HtmlFormatter",
             "JsonFormatter",
             "JsonpFormatter",
             "CsvFormatter",
             "ExcelFormatter",
             "AppFormatter",
           ]

@Processor.processor
class DataFormatter(Processor):

    def process(self):
        
        for emitter in EMITTERS:
            E = Emitter.get_emitter(emitter)
            e = E(self.token)
            if e.condition():
                L.debug("DataFormatter:: using emitter %s" % emitter)
                e.format()
                break
        else:
            emitter = "HtmlFormatter"
            E = Emitter.get_emitter(emitter)
            e = E(self.token)
            L.debug("DataFormatter:: using default emitter %s" % emitter)
            e.format()
        L.debug("DataFormatter:: token.response=%s (%s)" % (snip(repr(self.token.response)),self.token.content_type))
