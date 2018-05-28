import unittest
from bibliopixel.util import json

DATA = """
controls:
    -
        typename: midi

        extractor:
            accept:
              type: control_change

        routing:
            00: animation.limit.ratio
            01: animation.levels.knee
            02: animation.levels.gain
            09: animation.levels.enable  # yaml interprets this as a string '09'
            10: animation.levels.ratio
            020: animation.levels.knee   # yaml interprets this as octal
"""


class JsonTest(unittest.TestCase):
    def test_yaml_keys(self):
        result = json.loads(DATA, 'test.yml')
        routing = result['controls'][0]['routing']
        self.assertEqual(routing['0'], 'animation.limit.ratio')
        self.assertEqual(
            set(routing),
            set(('0', '1', '2', '09', '10', '16')))

        self.assertEqual(json.loads(DATA, use_yaml=True), result)

    def test_round_trip_json(self):
        result = json.loads(DATA, 'test.yml')
        saved = json.dumps(result)
        restored = json.loads(saved)
        self.assertEqual(result, restored)

    def test_round_trip_yaml(self):
        result = json.loads(DATA, 'test.yml')
        saved = json.dumps(result, use_yaml=True)
        restored = json.loads(saved, use_yaml=True)
        self.assertEqual(result, restored)
