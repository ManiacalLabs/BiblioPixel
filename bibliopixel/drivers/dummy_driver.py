from .. util import deprecated
if deprecated.allowed():  # pragma: no cover
    from . dummy import Dummy
    DriverDummy = Dummy
