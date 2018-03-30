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

// Contract object
var MyContract = web3.eth.contract(abi);

// instantiate by address
var contractInstance = MyContract.at(web3.eth.accounts[0]);

// set withholdings account
var withholdings_address = web3.eth.accounts[1]

// deploy new contract
var contractInstance = MyContract.new(withholdings_address, { // Not sure if .deploy or .new is to be used here. 
    data: '0x' + bytecode, // Why is <'0x'> required in front of bytecode ?
    from: web3.eth.coinbase, // Is this the address that sends the transaction?  
    gas: 2000000, // Gas limit (Where is the gas price set)
    });
    
console.log(contractInstance);












