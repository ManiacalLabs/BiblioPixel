from .. util import deprecated
if deprecated.allowed():
    from . dummy import Dummy
    DriverDummy = Dummy
