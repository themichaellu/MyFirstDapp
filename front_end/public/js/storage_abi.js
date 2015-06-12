var storage_abi = [{
{
    "name": "gain_access(int256)",
    "type": "function",
    "inputs": [{ "name": "contract_address", "type": "int256" }],
    "outputs": []
},


{
    "name": "has_access(int256)",
    "type": "function",
    "inputs": [{ "name": "contract_address", "type": "int256" }],
    "outputs": [{ "name": "out", "type": "int256" }]
},
{
    "name": "revoke_access(int256)",
    "type": "function",
    "inputs": [{ "name": "contract_address", "type": "int256" }],
    "outputs": []
},
{
    "name": "send(int256,int256)",
    "type": "function",
    "inputs": [{ "name": "address", "type": "int256" }, { "name": "amount", "type": "int256" }],
    "outputs": []
},
{
    "name": "update_creator(int256)",
    "type": "function",
    "inputs": [{ "name": "creator_address", "type": "int256" }],
    "outputs": []
}];
