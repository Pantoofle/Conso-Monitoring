from .interface import Interface
from .state import State


class LTE(Interface):
    """
    A class representing the LTE interface.
    """

    def __init__(self):
        super().__init__()
        self.states = self.build_states(["CRX", "DRX", "SDRX", "LDRX"])
        self.actual_state = self.states["DRX"]
        self.timeout = 0
        self.alpha_u = 1
        self.alpha_d = 1
        self.beta = 1

    def build_states(names):
        states = {}
        for n in names:
            states[n] = State(n)
        return states

    def consume_during(self, time, power=None):
        if power is None:
            power = self.actual_state.power_consumption

        self.consumed_energy += power * time

    def nothing_until(self, timestamp):
        delta = timestamp - self.time
        if delta < 0:
            # We missed the message, we read it now
            delta = 0

        # If there is a timeout waiting
        if self.actual_state.timeout is not None:
            timeout = self.actual_state.timeout
            time_until_timeout = timeout["time"] - self.timeout

            # If we timeout
            if delta > time_until_timeout:
                self.consume_during(time_until_timeout)
                if "transition" in timeout:
                    self. consume_during(timeout["transition_duration"],
                                         power=timeout["transition_power"])
                    self.time += timeout["transition_duration"]

                self.timeout = 0
                self.time += time_until_timeout
                self.actual_state = timeout["target"]
                self.nothing_until(timestamp)
        else:
            self.consume_during(delta)
            self.time += delta

    def transmission_power(self, up, down):
        return self.alpha_u * up + self.alpha_d * down + self.beta

    def handle_message(self, message):
        # If we have a trigger when receiving a message
        if self.actual_state.data is not None:
            transition = self.actual_state.data
            # If there is a transition cost
            if "transition" in transition:
                self. consume_during(transition["transition_duration"],
                                     power=transition["transition_power"])
                self.time += transition["transition_duration"]
            self.timeout = 0
            self.actual_state = transition["target"]
        # Send/receive the message
        up = self.upload
        down = self.download
        if message.direction == "upload":
            down = 0
        else:
            up = 0
        rate = up + down

        transmission_time = message.size/rate
        self.time += transmission_time
        self.consume_during(transmission_time, power=self.transmission_power(up, down))
