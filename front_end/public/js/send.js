
function load() {
    web3.setProvider(new web3.providers.HttpProvider('http://localhost:8545'));
    var coinbase = web3.eth.coinbase;
    console.log(coinbase);
    document.getElementById('coinbase').innerText = coinbase;
    var balance = web3.eth.getBalance(coinbase);
    console.log(balance.toString(10));
    document.getElementById('balance').innerText = web3.toDecimal(balance);
  };

function send() {
    console.log("Here we go")
    web3.setProvider(new web3.providers.HttpProvider('http://localhost:8545'));
    var coinbase = web3.eth.coinbase;
    var InterfaceContract = web3.eth.contract(interface_abi);
    console.log(InterfaceContract)
    var amount = document.getElementById("amount");
    console.log(amount.value)

    window.interface_contract = InterfaceContract.at('0x9847fb68d77fcfc2699df45392388f56498793ba');
    var total_sent = amount.value
    window.interface_contract.send_ether.sendTransaction(total_sent,
        {from: coinbase, value: total_sent, gas: 1000000000000000, gasPrice: 1,
        function (err) {
          if(!err) {
            console.log('send ether transaction sent.');
          }
          else {
            log_error(err);
          }
        }});

}
