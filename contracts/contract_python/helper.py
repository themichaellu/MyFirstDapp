from serpent_helpers import *


class AccessControl:

    def __init__(self):
        self.items = {}

    def __getitem__(self, contract):
        if str(contract) not in self.items:
            return 0
        return self.items[str(contract)]

    def __setitem__(self, key, value):
        self.items[str(key)] = value


class HelpersContract:

    def __init__(self):
        self.sa = None
        self.spa = None
        self.access_control = AccessControl()
        self.creator = None
        self.init()

    def __eq__(self, other):
        return True

    def init(self):
        self.creator = msg.sender

    def update_creator(self, creator_address, value=0):
        if msg.sender == self.creator:
            self.creator = creator_address

    def gain_access(self, contract_address, value=0):
        if msg.sender == self.creator and not self.access_control[contract_address]:
            self.access_control[contract_address] = 1

    def revoke_access(self, contract_address, value=0):
        if msg.sender == self.creator and self.access_control[contract_address]:
            self.access_control[contract_address] = 0

    def has_access(self, contract_address, value=0):
        return self.access_control[contract_address]

    def set_storage_address(self, storage_address, value=0):
        if msg.sender == self.creator:
            self.sa = storage_address

    def get_storage_address(self, value=0):
        return self.sa

    def send_ether_from_storage(receiver_address, amount):
        # either other functions of this contract or contracts with access rights
        if msg.sender == self or self.access_control[msg.sender]:
                self.sa.send(receiver_address, amount)
