from serpent_helpers import *


class InterfaceContract:

    def __init__(self):
        self.sa = None
        self.rma = None
        self.ha = None
        self.cma = None
        self.send_sa = None
        self.sell_sa = None
        self.spa = None
        self.baa = None
        self.bsa = None
        self.creator = None
        self.raa = None
        self.se = None
        self.init()

    def init(self):
        self.creator = msg.sender

    def update_creator(self, creator_address, value=0):
        if msg.sender == self.creator:
            self.creator = creator_address

    def get_storage_address(self, value=0):
        return self.sa

    def set_storage_address(self, storage_address, value=0):
        if msg.sender == self.creator:
            self.sa = storage_address

    def set_send_ether_address(self, send_ether_address, value=0):
        if msg.sender == self.creator:
            self.se = send_ether_address

    def get_send_ether_address(self, value=0):
        return self.se

    def send_ether(self, amount, value=0):
        sender_address = msg.sender
        self.se.send_ether(amount)
