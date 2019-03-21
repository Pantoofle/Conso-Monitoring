class State():
    """A class representing a state in the state machine of an interface"""

    def __init__(self, name):
        self.name = name
        self.timeout = None
        self.data = None
        self.power_consumption = 0
