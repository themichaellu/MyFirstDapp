
function load() {
	var input_name = localStorage.getItem("user_id");
	$('#name').text("Hi, " + input_name);
	web3.setProvider(new web3.providers.HttpProvider('http://localhost:8545'));
	var coinbase = web3.eth.coinbase;
	console.log(coinbase);
	$('#coinbase').text(coinbase);
	var balance = web3.eth.getBalance(coinbase);
	console.log(balance.toString(10));
	$('#balance').text(web3.toDecimal(balance));

}

function send() {
    console.log("Here we go")
    web3.setProvider(new web3.providers.HttpProvider('http://localhost:8545'));
    var coinbase = web3.eth.coinbase;
    var InterfaceContract = web3.eth.contract(interface_abi);
    console.log(InterfaceContract)
    var amount = $("#amount").val();
    console.log(amount)

    interface_contract = InterfaceContract.at('0x9847fb68d77fcfc2699df45392388f56498793ba');
    interface_contract.send_ether.sendTransaction(
			amount,
      {	from: coinbase,
				value: amount,
				gas: 1000000000000000,
				gasPrice: 1
			},
      function (err) {
        if(!err) {
          console.log('send ether transaction sent.');
        }
        else {
          console.log(err);
        }
      });

}
