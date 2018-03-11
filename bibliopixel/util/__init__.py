from . util import generate_header, even_dist, pointOnCircle, genVector

from . import deprecated
if deprecated.allowed():
    from . attribute_dict import AttributeDict
    d = AttributeDict
