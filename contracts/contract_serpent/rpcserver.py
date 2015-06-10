from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from ethereum import tester as t
from rlp.utils import encode_hex
from ethereum.utils import sha3
from ethereum.tester import keys

# CONFIG
BALANCE = 10000000000000000000000
GAS_PRICE = 10000000000000
GAS_LIMIT = 500000000
BLOCK_NUMBER = 1000
LOG_TRANSACTIONS = False
EXECUTE_LOGFILE = False
LOG_FILE = "last_transactions.txt"

# init state
s = t.state()
t.gas_limit = GAS_LIMIT
coinbase = s.block.coinbase

# create contracts
storage_contract = s.abi_contract('storage.se')
fact_server_contract = s.abi_contract('fact_server.se')
helpers_contract = s.abi_contract('helpers.se')
ln_n_contract = s.abi_contract('ln_n.se')
interface_contract = s.abi_contract('interface.se')

# gain access to storage
storage_contract.gain_access(coinbase)
storage_contract.gain_access(create_market_contract.address)
storage_contract.gain_access(resolve_market_contract.address)
storage_contract.gain_access(helpers_contract.address)
storage_contract.gain_access(send_shares_contract.address)
storage_contract.gain_access(buy_all_outcomes_contract.address)
storage_contract.gain_access(redeem_all_outcomes_contract.address)
storage_contract.gain_access(buy_shares_contract.address)
storage_contract.gain_access(sell_shares_contract.address)

# gain access to helpers
helpers_contract.gain_access(resolve_market_contract.address)
helpers_contract.gain_access(buy_shares_contract.address)
helpers_contract.gain_access(sell_shares_contract.address)
helpers_contract.gain_access(interface_contract.address)

# set create market addresses
create_market_contract.set_storage_address(storage_contract.address)
create_market_contract.set_interface_address(interface_contract.address)

# set resolve market addresses
resolve_market_contract.set_storage_address(storage_contract.address)
resolve_market_contract.set_helpers_address(helpers_contract.address)
resolve_market_contract.set_share_prices_address(share_prices_contract.address)
resolve_market_contract.set_interface_address(interface_contract.address)

# set helpers addresses
helpers_contract.set_storage_address(storage_contract.address)
helpers_contract.set_share_prices_address(share_prices_contract.address)

# set send shares addresses
send_shares_contract.set_storage_address(storage_contract.address)
send_shares_contract.set_interface_address(interface_contract.address)

# set buy all outcomes addresses
buy_all_outcomes_contract.set_storage_address(storage_contract.address)
buy_all_outcomes_contract.set_interface_address(interface_contract.address)

# set redeem all outcomes addresses
redeem_all_outcomes_contract.set_storage_address(storage_contract.address)
redeem_all_outcomes_contract.set_helpers_address(helpers_contract.address)
redeem_all_outcomes_contract.set_interface_address(interface_contract.address)

# set buy shares addresses
buy_shares_contract.set_storage_address(storage_contract.address)
buy_shares_contract.set_share_prices_address(share_prices_contract.address)
buy_shares_contract.set_helpers_address(helpers_contract.address)
buy_shares_contract.set_interface_address(interface_contract.address)

# set sell shares addresses
sell_shares_contract.set_storage_address(storage_contract.address)
sell_shares_contract.set_share_prices_address(share_prices_contract.address)
sell_shares_contract.set_helpers_address(helpers_contract.address)
sell_shares_contract.set_interface_address(interface_contract.address)

# set interface addresses
interface_contract.set_storage_address(storage_contract.address)
interface_contract.set_create_market_address(create_market_contract.address)
interface_contract.set_share_prices_address(share_prices_contract.address)
interface_contract.set_resolve_market_address(resolve_market_contract.address)
interface_contract.set_send_shares_address(send_shares_contract.address)
interface_contract.set_buy_all_outcomes_address(buy_all_outcomes_contract.address)
interface_contract.set_redeem_all_outcomes_address(redeem_all_outcomes_contract.address)
interface_contract.set_buy_shares_address(buy_shares_contract.address)
interface_contract.set_sell_shares_address(sell_shares_contract.address)
interface_contract.set_helpers_address(helpers_contract.address)

# set share prices addresses
share_prices_contract.set_share_prices_address_1(share_prices_1_contract.address)
share_prices_contract.set_share_prices_address_2(share_prices_2_contract.address)
share_prices_contract.set_ln_n_address(ln_n_address_contract.address)

# set parameters
share_prices_contract.set_precision_factor(1000000000000)
share_prices_contract.set_outcome_range(10000)

# execute transactions
if EXECUTE_LOGFILE:
    transactions = [line.strip().split('\t') for line in open(LOG_FILE) if line]
    for tx in transactions:
        s.send(keys[0], interface_contract.address, int(tx[1]), evmdata=tx[2].decode('hex'))

# log transactions
if LOG_TRANSACTIONS:
    log_file = open(LOG_FILE, 'a+')

print "Ready!"


def int_to_hex(int_value):
    encoded = format(int_value, 'x')
    return encoded.zfill(len(encoded)*2 % 2)


def eth_coinbase():
    print 'eth_coinbase'
    return '0x' + encode_hex(coinbase)


def eth_getBalance(address, block_number):
    print 'eth_getBalance'
    return '0x' + int_to_hex(BALANCE)


def eth_gasPrice():
    print 'eth_gasPrice'
    return '0x' + int_to_hex(GAS_PRICE)


def eth_blockNumber():
    print 'eth_blockNumber'
    return '0x' + int_to_hex(BLOCK_NUMBER)


def eth_call(transaction, block_number):
    print 'eth_call'
    return '0x' + s.send(keys[0], interface_contract.address, 0, evmdata=transaction['data'][2:].decode('hex')).encode('hex')


def eth_sendTransaction(transaction):
    print 'eth_sendTransaction'
    global BALANCE
    global BLOCK_NUMBER
    t.gas_limit = GAS_LIMIT
    value = int(transaction['value'], 16)
    BALANCE -= value
    BLOCK_NUMBER += 1
    if transaction['data'].startswith('0x4891e225'):
        contract_address = fact_server_contract.address
    else:
        contract_address = interface_contract.address
    if LOG_TRANSACTIONS:
        log_file.write('{}\t{}\t{}\n'.format(contract_address.encode('hex'), value, transaction['data'][2:]))
    s.send(keys[0], contract_address, value, evmdata=transaction['data'][2:].decode('hex'))


def web3_sha3(argument):
    print 'web3_sha3'
    return '0x' + sha3(argument[2:].decode('hex')).encode('hex')


server = SimpleJSONRPCServer(('localhost', 8545))
server.register_function(eth_coinbase, 'eth_coinbase')
server.register_function(eth_getBalance, 'eth_getBalance')
server.register_function(web3_sha3, 'web3_sha3')
server.register_function(eth_gasPrice, 'eth_gasPrice')
server.register_function(eth_blockNumber, 'eth_blockNumber')
server.register_function(eth_call, 'eth_call')
server.register_function(eth_sendTransaction, 'eth_sendTransaction')
server.serve_forever()
