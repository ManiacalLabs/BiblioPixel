class d(dict):
    def __init__(self, *a, **k):
        super(d, self).__init__(*a, **k)
        self.__dict__ = self
        for k in self.__dict__:
        	if isinstance(self.__dict__[k], dict):
        		self.__dict__[k] = d(self.__dict__[k])
        	elif isinstance(self.__dict__[k], list):
        		for i in range(len(self.__dict__[k])):
        			if isinstance(self.__dict__[k][i], dict):
        				self.__dict__[k][i] = d(self.__dict__[k][i])
    def upgrade(self, a):
        for k,v in a.items():
            if not k in self:
                self[k] = v
