import io, tempfile, unittest
from bibliopixel.util import data_file
from bibliopixel.util.persistent_dict import PersistentDict

DATA_FILE_TEST = """
{
  "a": {"foo": "bar", "bang": 1}
}
"""


class PersistentDictTest(unittest.TestCase):
    def test_reader_writer_data_file(self):
        with tempfile.NamedTemporaryFile('w') as tf:
            tf.write(DATA_FILE_TEST)
            tf.seek(0)

            pd = PersistentDict(tf.name)
            self.assertEqual(pd, {'a': {'foo': 'bar', 'bang': 1}})
            pd.clear()
            self.assertEqual(pd, {})
            self.assertEqual(data_file.load(tf.name), pd)

            pd.update(bang={'hi': 'there'})
            self.assertEqual(pd, {'bang': {'hi': 'there'}})
            self.assertEqual(data_file.load(tf.name), pd)
