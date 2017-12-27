import io, unittest
from .. import mock
from bibliopixel.util import json
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
        filesystem = {'test.json': JSON_TEST}
        with mock.patch_open(filesystem, json):
            datafile = DataFile('test.json')
            datafile.read()
            self.assertEqual(datafile.data, {'a': {'foo': 'bar', 'bang': 1}})
            datafile.data = {'bang': {'hi': 'there'}}
            datafile.write()
            self.assertEqual(json.loads(filesystem['test.json']), datafile.data)
