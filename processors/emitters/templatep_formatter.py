import json

from base import Emitter
from internal_db_ops import internal_find
from processors.emitters.template_formatter import TemplateFormatter

@Emitter.emitter
class TemplatePFormatter(TemplateFormatter):
    
    def condition(self):
        self.callback = self.token.request.args.get('callback',None)
        format = self.token.get_request_format()
        return super(TemplatePFormatter,self).condition() and self.callback != None and format.startswith("templatep")
    
    def format(self):
        super(TemplatePFormatter,self).format()
        self.token.content_type = 'text/javascript'
        self.token.response = "%s(%s);" % (self.callback, json.dumps(self.token.response))
