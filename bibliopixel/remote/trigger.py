class TriggerBase:
    def __init__(self, q, events):
        self.q = q
        self.events = events

    def trigger(self, name):
        self.q.put(
            {'req': 'trigger_animation', 'data': name, 'sender': 'Trigger'})
