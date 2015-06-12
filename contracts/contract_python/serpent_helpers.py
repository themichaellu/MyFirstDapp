# serpent build in functions
receivers = {}

TYPE_N_OUTCOMES = 0
TYPE_NUMERIC = 1
BUY = 0
SELL = 1


class Message:

    def __init__(self, sender=None, value=None):
        self.sender = sender
        self.value = value


class Block:

    def __init__(self, timestamp=None):
        self.timestamp = timestamp


def set_msg(sender, value=0):
    global msg
    msg.sender = sender
    msg.value = value


def set_block(timestamp):
    global block
    block.timestamp = timestamp

msg = Message()
block = Block()


class Receivers:

    def __init__(self):
        self.items = {}

    def __getitem__(self, item):
        if not str(item) in self.items:
            self.items[str(item)] = 0
        return self.items[str(item)]

    def __setitem__(self, key, value):
        self.items[str(key)] = value

receivers = Receivers()


def send(to, value):
    print('sending {} to {}'.format(value, to))
    global receivers
    receivers_value = receivers[to]
    receivers[to] = receivers_value + value


def load(arr, items=0):
    return arr[:items]


def array(length):
    return [0] * length

