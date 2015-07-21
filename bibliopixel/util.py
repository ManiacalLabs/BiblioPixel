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

def tuple_add(a, b):
    return tuple(x + y for x,y in zip(a, b))

def tuple_sub(a, b):
    return tuple(x - y for x,y in zip(a, b))

def tuple_mult(a, b):
    return tuple(x * y for x,y in zip(a, b))

def tuple_div(a, b):
    return tuple(x / y for x,y in zip(a, b))
