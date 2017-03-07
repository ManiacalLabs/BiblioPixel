import io, json, unittest
from .mock import mock_open

from bibliopixel.util import datafile

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
        reader, writer = datafile.reader_writer('test.json', open=mopen)

        self.assertEqual(reader(), {'a': {'foo': 'bar', 'bang': 1}})
        d = {'bang': {'hi': 'there'}}
        writer(d)
        self.assertEqual(json.loads(context['test.json']), d)

    def test_reader_writer_config(self):
        context = {'.test': CONFIG_TEST}
        mopen = mock_open(context)
        reader, writer = datafile.reader_writer('.test', open=mopen)
        result = {
            'DEFAULT': {},
            'a': {'foo': 'bar', 'bang': '1'},
        }
        self.assertEqual(reader(), result)

        d = {'bang': {'hi': 'there'}}
        writer(d)
        fp = io.StringIO(context['.test'])
        config = datafile.read_config(fp)
        self.assertEqual(config, dict(d, DEFAULT={}))
