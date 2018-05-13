import collections


class Extractor:
    """
    Extractor is a class that extracts and normalizes values from
    incoming message dictionaries into ordered dictionaries based on the
    `type` key of each message.
    """

    def __init__(self, omit=None, normalizers=None, keys_by_type=None,
                 accept=None, reject=None, auto_omit=True):
        """
        Arguments

        omit -- A list of keys that will not be extracted.

        normalizers -- Some keys also need to be "normalized" -
            scaled and offset so they are between 0 and 1, or -1 and 1.
            The `normalizers` table maps key names to a function that
            normalizes the value of that key.

        keys_by_type -- `keys_by_type` is a dictionary from the `type` in an
            incoming message to a list of message keys to be extracted

        accept -- maps keys to a value or a list of values that are
            accepted for that key.  A message has to match *all* entries in
            `accept` to be accepted.

        reject -- map key to a value or a list of values that are not
            accepted for that key.  A message is rejected if it matches *any*
            entry in the reject map.

        auto_omit -- if True, omit all keys in `accept` that only have one
            possible value.

            auto_omit=True, the default, is probably more useful: if you
            request data for channel=1, type=note_on then you probably don't
            want to see channel=1, type=note_on with each message.
        """
        def to_set(x):
            if x is None:
                return set()
            if isinstance(x, (list, tuple)):
                return set(x)
            return set([x])

        def make_match(m):
            return m and {k: to_set(v) for k, v in m.items()}

        self.accept, self.reject = make_match(accept), make_match(reject)
        self.omit = to_set(omit)
        if auto_omit and self.accept:
            self.omit.update(k for k, v in self.accept.items() if len(v) == 1)

        self.normalizers = normalizers or {}
        if keys_by_type is None:
            self.keys_by_type = None
        else:
            self.keys_by_type = {}
            for k, v in keys_by_type.items():
                if isinstance(v, str):
                    v = [v]
                self.keys_by_type[k] = tuple(i for i in v if i not in self.omit)

    def extract(self, msg):
        """Yield an ordered dictionary if msg['type'] is in keys_by_type."""
        def normal(key):
            v = msg.get(key)
            if v is None:
                return v
            normalizer = self.normalizers.get(key, lambda x: x)
            return normalizer(v)

        def odict(keys):
            return collections.OrderedDict((k, normal(k)) for k in keys)

        def match(m):
            return (msg.get(k) in v for k, v in m.items()) if m else ()

        accept = all(match(self.accept))
        reject = any(match(self.reject))

        if reject or not accept:
            keys = ()
        elif self.keys_by_type is None:
            keys = [k for k in msg.keys() if k not in self.omit]
        else:
            keys = self.keys_by_type.get(msg.get('type'))
        return odict(keys)
