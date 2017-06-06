import io, json, unittest
from . mock import mock_open

from bibliopixel.util.datafile import DataFile

DEFAULTS = {
    'a': {'foo': 0, 'bang': 0, 'burt': 0},
}

JSON_TEST = """
{
  "a": {"foo": "bar", "bang": 1}
}
"""


class DatafileTest(unittest.TestCase):
    def test_reader_writer_json(self):
        context = {'test.json': JSON_TEST}
        mopen = mock_open(context)
        datafile = DataFile('test.json', open=mopen)
        datafile.read()
        self.assertEqual(datafile.data, {'a': {'foo': 'bar', 'bang': 1}})
        datafile.data = {'bang': {'hi': 'there'}}
        datafile.write()
        self.assertEqual(json.loads(context['test.json']), datafile.data)
