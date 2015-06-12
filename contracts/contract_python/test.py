from interface import InterfaceContract
from storage import StorageContract
from send_ether import SendEtherContract

from serpent_helpers import set_msg, set_block, receivers, SELL, TYPE_NUMERIC, TYPE_N_OUTCOMES, BUY
import unittest


class TestContract(unittest.TestCase):

    def setUp(self):
        sender = 0
        timestamp = 1428220562

        set_msg(sender=sender, value=0)
        set_block(timestamp=timestamp)

        # create contracts
        self.storage_contract = StorageContract()
        self.interface_contract = InterfaceContract()
        self.send_ether_contract = SendEtherContract()

        # gain access for creator
        self.storage_contract.gain_access(sender)

        # gain access to storage

        # set send shares addresses
        self.send_ether_contract.set_storage_address(self.storage_contract)

        # set interface addresses
        self.interface_contract.set_storage_address(self.storage_contract)
        self.interface_contract.set_send_ether_address(self.send_ether_contract)


    def set_msg(self, sender, value=0):
        self.storage_contract.access_control[sender] = 1
        set_msg(sender=sender, value=value)

    def reset(self):
        receivers.items = {}

    def test_send_ether(self):
        self.set_msg(sender=1, value=0)
        self.interface_contract.send_ether(123431, value=0)
        print(receivers[1])
        print(receivers[self.interface_contract.get_storage_address()])










if __name__ == '__main__':
    unittest.main()