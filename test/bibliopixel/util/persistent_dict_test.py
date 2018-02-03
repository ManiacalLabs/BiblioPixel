import io, unittest
from .. import mock
from bibliopixel.util import json
from bibliopixel.util.persistent_dict import PersistentDict

DEFAULTS = {
    'a': {'foo': 0, 'bang': 0, 'burt': 0},
}

JSON_TEST = """
{
  "a": {"foo": "bar", "bang": 1}
}
"""


class Persistent_dictTest(unittest.TestCase):
    def test_reader_writer_json(self):
        filesystem = {'test.json': JSON_TEST}
        with mock.patch_open(filesystem, json):
            pd = PersistentDict('test.json')
            pd.read()
            self.assertEqual(pd.data, {'a': {'foo': 'bar', 'bang': 1}})
            pd.data = {'bang': {'hi': 'there'}}
            pd.write()
            self.assertEqual(json.loads(filesystem['test.json']), pd.data)
