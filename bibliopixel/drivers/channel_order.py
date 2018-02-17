class ChannelOrder(object):
    """
    Helper class to automatically convert string values into tuple
    values needed to define color channel order.
    """

    RGB = 0, 1, 2
    RBG = 0, 2, 1
    GRB = 1, 0, 2
    GBR = 1, 2, 0
    BRG = 2, 0, 1
    BGR = 2, 1, 0

    ORDERS = RGB, RBG, GRB, GBR, BRG, BGR

    @staticmethod
    def make(x):
        orders = ChannelOrder.ORDERS
        try:
            length = len(x)
        except:
            # Must be an integer index.
            if x < 0:
                raise ValueError(
                    'ChannelOrder index %s is not between 0 and 5' % x)
            try:
                return orders[x]
            except IndexError:
                raise ValueError(
                    'ChannelOrder index %s is not between 0 and 5' % x)
            except:
                raise ValueError(
                    'ChannelOrder index "%s" is not an integer' % x)

        if length != 3:
            raise ValueError('ChannelOrder "%s" does not have length 3' % x)

        try:
            s = x.lower()
        except AttributeError:
            s = tuple(x)
        else:
            try:
                s = tuple('rgb'.index(i) for i in s)
            except ValueError:
                raise ValueError('ChannelOrder "%s" has non-rgb elements' % x)

        if not all(0 <= x <= 2 for x in s):
            raise ValueError(
                'ChannelOrder %s has members not between 0 and 2.' % x)

        try:
            # Canonicalize and detect dupes at the same time.
            return orders[orders.index(s)]
        except:
            raise ValueError('ChannelOrder %s has duplicate elements' % x)
