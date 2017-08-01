from .. util import importer


class TriggerBase:
    def __init__(self, q, configs):
        self.q = q
        self.configs = configs

    def trigger(self, name):
        self.q.put({'req': 'trigger_animation', 'data': name, 'sender': 'Trigger'})
