from . extractor import Extractor


class ControlSource(Extractor):
    """
    A ControlSource is an iterator that yields output messages by running an
    Extractor on messages from an input iterator.

    Usage:

        for extracted_msg in MyControlSource():
            # Process extracted message.

    A ControlSource is an abstract base class: a derived class needs to
    implement the method `make_iterator` which takes an input description and
    yields a series of input messages to be extracted.
    """

    KEYS_BY_TYPE = {}
    NORMALIZERS = {}

    def __init__(self, *, input=None, **kwds):
        """
        Arguments

        input -- input description.  This is passed to self.make_iterator to
            construct the input iterator.
        kwds -- keyword options passed to the  constructor of Extractor.
        """
        super().__init__(
            normalizers=self.NORMALIZERS,
            keys_by_type=self.KEYS_BY_TYPE,
            **kwds)
        self.input = input
        self.iterator = None

    def __iter__(self):
        """Yield a series of extracted messages from the input"""
        self.pre_run()
        for msg in self.iterator:
            yield from self.extract(msg)

    def pre_run(self):
        """
        Construct the input iterator before iterating over it.

        It might take some actual time to initialize the input stream with
        self.make_iterator. Call `self.pre_run()` before the actual iteration
        starts to avoid a delay in extracting the first message.
        """
        self.iterator = self.iterator or self.make_iterator(self.input)

    def make_interator(self, input):
        raise NotImplementedError
