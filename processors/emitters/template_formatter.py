import pystache

from base import Emitter
from internal_db_ops import internal_find

@Emitter.emitter
class TemplateFormatter(Emitter):
    
    def condition(self):
        self.format = self.token.get_request_format()
        self.template_name = ("%s:" % self.format).split(':')[1]
        return format.startswith('template')
    
    def format(self):
        self.token.content_type = 'text/html'
        templates = internal_find( self.token.path, fields=["templates"] )
        if self.template_name == "":
            if self.token.slug == None:
                template = templates.get('template__detail')
            else: 
                template = templates.get('template__list')
        else:
            template = templates.get('template__%s' % self.template_name)
            
        self.token.response = pystache.render(template,{"response":self.token.response})
