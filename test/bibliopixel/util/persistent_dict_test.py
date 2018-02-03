import io, tempfile, unittest
from bibliopixel.util import json
from bibliopixel.util.persistent_dict import PersistentDict

JSON_TEST = """
{
  "a": {"foo": "bar", "bang": 1}
}
"""


class PersistentDictTest(unittest.TestCase):
    def test_reader_writer_json(self):
        with tempfile.NamedTemporaryFile('w') as tf:
            tf.write(JSON_TEST)
            tf.seek(0)

            pd = PersistentDict(tf.name)
            self.assertEqual(pd, {'a': {'foo': 'bar', 'bang': 1}})
            pd.clear()
            self.assertEqual(pd, {})
            self.assertEqual(json.load(tf.name), pd)

            pd.update(bang={'hi': 'there'})
            self.assertEqual(pd, {'bang': {'hi': 'there'}})
            self.assertEqual(json.load(tf.name), pd)
