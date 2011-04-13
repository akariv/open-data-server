from base import Emitter
from StringIO import StringIO

@Emitter.emitter
class HtmlFormatter(Emitter):
    
    def condition(self):
        format = self.token.get_request_format()
        return format == 'html'
    
    def html_for_obj(self,obj):
        out = StringIO()
        if type(obj) == list:
            out.write("<table border='1'>")
            fields = set()
            for rec in obj:
                fields.update(rec.keys())
            fields = list(fields)
            out.write('<tr><th>')
            out.write(u'</th><th>'.join(fields))
            out.write('</th></tr>')
            for rec in obj:
                out.write('<tr><td>')
                out.write('</td><td>'.join([self.html_for_obj(rec.get(f,'')) for f in fields]))
                out.write('</th></tr>')
            out.write("</table>")

        elif type(obj) == dict:
            out.write("<table border='1'>")
            for k,v in obj.iteritems():
                out.write('<tr><td>%s:</td><td>%s</td></tr>' % (k,self.html_for_obj(v)))
            out.write("</table>")
        
        else:
            return unicode(obj)
                
        return out.getvalue()
    
    def format(self):
        self.token.content_type = 'text/html'
        out = StringIO()
        out.write("<html><body>")
        out.write(self.html_for_obj(self.token.response))
        out.write("</body></html>")
        self.token.response = out.getvalue()
