from . base import TypesBaseTest


class DurationTypesTest(TypesBaseTest):
    def test_some(self):
        self.make('duration', '1', 1)
        self.make('duration', '1s', 1)
        self.make('duration', '2.5s', 2.5)
        self.make('duration', '10 mins, 2.5s', 602.5)
