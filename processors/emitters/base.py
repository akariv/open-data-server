class Emitter(object):
    
    available_emitters = {}
    
    def __init__(self,token):
        self.token = token
    
    def format(self):
        assert(False)

    @classmethod
    def get_emitter(cls,name):
        return cls.available_emitters.get(name)

    @classmethod
    def emitter(cls,klass):
        cls.available_emitters[klass.__name__]=klass
        return klass
    
