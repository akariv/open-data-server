from base import Emitter
from internal_db_ops import internal_find

@Emitter.emitter
class StaticFileFormatter(Emitter):
    
    STATIC_SUFFIX = '/static'
    
    def condition(self):
        format = self.token.get_request_format()
        return self.token.path.endswith(self.STATIC_SUFFIX) and self.token.slug != None and format == None
    
    def format(self):
        real_path = self.token.path[:-len(self.STATIC_SUFFIX)]
        statics = internal_find( real_path, fields=["statics"] ).get("statics",{})
        self.token.content_type, self.token.response = statics.get(self.token.slug,("text/html",""))
