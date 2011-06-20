import pystache

from base import Emitter
from internal_db_ops import internal_find

@Emitter.emitter
class TemplateFormatter(Emitter):
    
    def condition(self):
        format = self.token.get_request_format()
        if not (format.startswith('template') or format == None):
            return False
        try:
            templates = internal_find( self.token.path, fields=["templates"] ).get("templates",{})
        except:
            return False
        self.template_name = ("%s:" % format).split(':')[1]
        if self.template_name == "":
            if self.token.slug != None:
                self.template = templates.get('detail')
            else: 
                self.template = templates.get('list')
        else:
            self.template = templates.get('%s' % self.template_name)
        return self.template != None 
    
    def format(self):
        self.token.content_type = 'text/html'                        
        self.token.response = pystache.render(self.template,response = self.token.response)
