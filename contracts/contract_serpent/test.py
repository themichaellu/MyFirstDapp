from unittest import TestCase, main
from ethereum import tester as t
from rlp.utils import encode_hex
from ethereum.tester import keys, accounts


class TestContract(TestCase):

    def setUp(self):
        self.s = t.state()
        t.gas_limit = 3141592

        self.coinbase = encode_hex(self.s.block.coinbase)

        # create contracts
        self.storage_contract = self.s.abi_contract('storage.se')
        self.interface_contract = self.s.abi_contract('interface.se')
        self.send_ether_contract = self.s.abi_contract('send_ether.se')

        # gain access to storage
        self.storage_contract.gain_access(self.coinbase)
        self.storage_contract.gain_access(self.send_ether_contract.address)

        # set send shares addresses
        self.send_ether_contract.set_storage_address(self.storage_contract.address)
        self.send_ether_contract.set_storage_address(self.interface_contract.address)

        # set interface addresses
        self.interface_contract.set_storage_address(self.storage_contract.address)
        self.interface_contract.set_send_ether_address(self.send_ether_contract.address)


    def test_send_ether(self):
        buyer_1 = 1
        total = 10000000000
        self.interface_contract.send_ether(123431, value=total, sender = keys[buyer_1])

        # print(receivers[1])
        # print(receivers[self.interface_contract.get_storage_address()])










if __name__ == '__main__':
    main()
