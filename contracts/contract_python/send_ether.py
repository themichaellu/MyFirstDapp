from serpent_helpers import *
class SendEtherContract:

    def __init__(self):
        self.sa = None
        self.creator = None
        self.init()

    def init(self):
        self.creator = msg.sender

    def update_creator(self, creator_address, value=0):
        if msg.sender == self.creator:
            self.creator = creator_address

    def set_storage_address(self, storage_address, value=0):
        if msg.sender == self.creator:
            self.sa = storage_address

    def get_storage_address(self, value=0):
        return self.sa

    def send_ether(self, amount):

        self.sa.send(self.sa, amount)
