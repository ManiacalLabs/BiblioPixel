import io, json, unittest
from .mock import mock_open

from bibliopixel.util.datafile import load_config, DataFile

DEFAULTS = {
    'a': {'foo': 0, 'bang': 0, 'burt': 0},
}

JSON_TEST = """
{
  "a": {"foo": "bar", "bang": 1}
}
"""

CONFIG_TEST = """

[a]
  foo=bar
  bang=1

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

    def test_reader_writer_config(self):
        context = {'.test': CONFIG_TEST}
        mopen = mock_open(context)
        datafile = DataFile('.test', open=mopen)
        datafile.read()

        result = {'a': {'foo': 'bar', 'bang': '1'}}
        self.assertEqual(datafile.data, result)

        datafile.data = {'bang': {'hi': 'there'}}
        datafile.write()

        fp = io.StringIO(context['.test'])
        config = load_config(fp)
        self.assertEqual(config, datafile.data)
