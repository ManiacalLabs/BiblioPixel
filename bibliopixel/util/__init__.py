from . import deprecated
if deprecated.allowed():  # pragma: no cover
    from . util import generate_header, even_dist, pointOnCircle, genVector
    from . attribute_dict import AttributeDict
    d = AttributeDict
