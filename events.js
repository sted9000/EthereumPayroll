const fs = require('fs'); // File system manager
const solc = require('solc'); // Solidity compiler (How do I know that there were no errors during compile?)
const Web3 = require('web3'); // Ethereum JavaScript API that allows local connections. 

// Connect to local Ethereum node (How do I set this up with geth, testrpc, geth --rpc ???)
const web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));

// Compile the source code
const input = fs.readFileSync('DQPayroll.sol'); 
const output = solc.compile(input.toString(), 1);
const bytecode = output.contracts[':DQPayroll'].bytecode; // This is tricky: i - Make sure .sol filename is same as contract name and that you prepend contract name with <:>
const abi = JSON.parse(output.contracts[':DQPayroll'].interface);

// Connect contract 
web3.eth.defaultAccount = web3.eth.accounts[1];
var DQPayroll = web3.eth.contract(abi); // Contract object
var DQPayroll_address = '0x76b2ec7656a3a921f00851d8f32f9b8891bc38aa' // contract address (copy and pasted)
var contract_interface = DQPayroll.at(DQPayroll_address); // js contract interaction variable
var events = contract_interface.allEvents({}, 'latest'); // Watching events and returning the latest 
var events_log = [];
events.watch(function(error, result) {
    if (!error)
        console.log(result);
    	events_log.push(result);
    	console.log(events_log.length);
});









