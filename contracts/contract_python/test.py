from storage import StorageContract, Markets, Shareholders, MarketHashes
from create_market import CreateMarketContract
from buy_all_outcomes import BuyAllOutcomesContract
from buy_shares import BuySharesContract
from fact_server import FactServerContract
from helpers import HelpersContract
from interface import InterfaceContract
from redeem_all_outcomes import RedeemAllOutcomesContract
from resolve_market import ResolveMarketContract
from sell_shares import SellSharesContract
from send_shares import SendSharesContract
from share_prices import SharePricesContract
from share_prices_1 import SharePrices1Contract
from share_prices_2 import SharePrices2Contract
from ln_n import LnNContract

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
        self.fact_server_contract = FactServerContract()
        self.create_market_contract = CreateMarketContract()
        self.resolve_market_contract = ResolveMarketContract()
        self.buy_shares_contract = BuySharesContract()
        self.buy_all_outcomes_contract = BuyAllOutcomesContract()
        self.redeem_all_outcomes_contract = RedeemAllOutcomesContract()
        self.helpers_contract = HelpersContract()
        self.send_shares_contract = SendSharesContract()
        self.sell_shares_contract = SellSharesContract()
        self.share_prices_contract = SharePricesContract()
        self.share_prices_1_contract = SharePrices1Contract()
        self.share_prices_2_contract = SharePrices2Contract()
        self.ln_n_contract = LnNContract()
        self.interface_contract = InterfaceContract()

        # gain access for creator
        self.storage_contract.gain_access(sender)
        self.helpers_contract.gain_access(sender)

        # gain access to storage
        self.storage_contract.gain_access(self.create_market_contract)
        self.storage_contract.gain_access(self.resolve_market_contract)
        self.storage_contract.gain_access(self.helpers_contract)
        self.storage_contract.gain_access(self.send_shares_contract)
        self.storage_contract.gain_access(self.buy_all_outcomes_contract)
        self.storage_contract.gain_access(self.redeem_all_outcomes_contract)
        self.storage_contract.gain_access(self.buy_shares_contract)
        self.storage_contract.gain_access(self.sell_shares_contract)

        # gain access to helpers
        self.helpers_contract.gain_access(self.resolve_market_contract)
        self.helpers_contract.gain_access(self.buy_shares_contract)
        self.helpers_contract.gain_access(self.sell_shares_contract)

        # set create market addresses
        self.create_market_contract.set_storage_address(self.storage_contract)

        # set resolve market addresses
        self.resolve_market_contract.set_storage_address(self.storage_contract)
        self.resolve_market_contract.set_helpers_address(self.helpers_contract)
        self.resolve_market_contract.set_share_prices_address(self.share_prices_contract)

        # set helpers addresses
        self.helpers_contract.set_storage_address(self.storage_contract)
        self.helpers_contract.set_share_prices_address(self.share_prices_contract)

        # set send shares addresses
        self.send_shares_contract.set_storage_address(self.storage_contract)

        # set buy all outcomes addresses
        self.buy_all_outcomes_contract.set_storage_address(self.storage_contract)

        # set redeem all outcomes addresses
        self.redeem_all_outcomes_contract.set_storage_address(self.storage_contract)
        self.redeem_all_outcomes_contract.set_helpers_address(self.helpers_contract)

        # set buy shares addresses
        self.buy_shares_contract.set_storage_address(self.storage_contract)
        self.buy_shares_contract.set_share_prices_address(self.share_prices_contract)
        self.buy_shares_contract.set_helpers_address(self.helpers_contract)

        # set sell shares addresses
        self.sell_shares_contract.set_storage_address(self.storage_contract)
        self.sell_shares_contract.set_share_prices_address(self.share_prices_contract)
        self.sell_shares_contract.set_helpers_address(self.helpers_contract)

        # set interface addresses
        self.interface_contract.set_storage_address(self.storage_contract)
        self.interface_contract.set_share_prices_address(self.share_prices_contract)
        self.interface_contract.set_create_market_address(self.create_market_contract)
        self.interface_contract.set_resolve_market_address(self.resolve_market_contract)
        self.interface_contract.set_send_shares_address(self.send_shares_contract)
        self.interface_contract.set_buy_all_outcomes_address(self.buy_all_outcomes_contract)
        self.interface_contract.set_redeem_all_outcomes_address(self.redeem_all_outcomes_contract)
        self.interface_contract.set_buy_shares_address(self.buy_shares_contract)
        self.interface_contract.set_sell_shares_address(self.sell_shares_contract)

        # set share prices addresses
        self.share_prices_contract.set_share_prices_address_1(self.share_prices_1_contract)
        self.share_prices_contract.set_share_prices_address_2(self.share_prices_2_contract)
        self.share_prices_contract.set_ln_n_address(self.ln_n_contract)

        # set parameters
        self.share_prices_contract.set_precision_factor(1000000000000)
        self.share_prices_contract.set_outcome_range(10000)


    def set_msg(self, sender, value=0):
        self.storage_contract.access_control[sender] = 1
        self.helpers_contract.access_control[sender] = 1
        set_msg(sender=sender, value=value)

    def reset(self):
        receivers.items = {}

    def test_buy_shares(self):
        self.reset()
        market_balance = 1000
        market_hash = self.create_event(value=market_balance, outcome_count=3)
        outcome = 1
        max_price = int(0.34565 * 1000000000000)
        self.set_msg(sender=1, value=2000000)
        self.interface_contract.buy_shares(market_hash, outcome, max_price, shares_to_spent=0, create_open_order=0, cancellation_date=0)
        # spent money should be 19
        # fee = self.sa.get_market_fee(market_hash, value=0)
        # TODO: Move fee testing to another independent more thorough test
        spent_money = 18
        fee = self.storage_contract.get_market_fee(market_hash, value=0)
        if fee:
            self.assertEqual(self.storage_contract.get_market_balance(market_hash), market_balance + 6560 + (6560 * fee / 100000))
        else:
            self.assertEqual(self.storage_contract.get_market_balance(market_hash), market_balance + spent_money)








if __name__ == '__main__':
    unittest.main()