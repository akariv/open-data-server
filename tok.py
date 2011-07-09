class Token(object):
    
    def __init__(self,request,path,slug,user):
        self.path = path
        self.slug = slug
        self.request = request
        self.data = self.request.data
        self.response = ''
        self.content_type = ''
        self.headers = {}
        self.lang = None
        self.user = user

    def get_request_format(self):
        return self.request.args.get('o',None)