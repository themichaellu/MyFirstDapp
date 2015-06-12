(function ($) {
  $(document).ready(function(){
      window.web3 = require('web3');
      web3.setProvider(new web3.providers.HttpProvider('http://' + $('#host').val() + ':' + $('#port').val()));
      var ServerContract = web3.eth.contract(server_abi);
      server_contract = new ServerContract($('#server_contract_address').val());
      });
})(jQuery);
