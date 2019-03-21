from .state import State


class Interface:
    """
    A class representing an interface.
    It holds the state machine and energy consumption costs.
    When given a packet trafic, it can output the total cost of transmiting such trafic
    """

    def __init__(self, name):
        self.name = name
        self.consumed_energy = 0
        self.time = 0
        self.upload = 10
        self.download = 10

    def reset(self):
        self.consumed_energy = 0

    def nothing_until(self, timestamp):
        raise NotImplementedError()

    def handle_message(self, message):
        raise NotImplementedError()

    def step(self, message):
        self.nothing_until(message.timestamp)
        self.handle_message(message)

    def run(self, trafic):
        for message in trafic:
            self.step(message)
