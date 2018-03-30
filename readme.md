# DQ Ethereum Payroll

## About:
A simple solidity contract that pays employees eth based on hours worked. 

## v0.0.2:
* Locally functional
* One contract (stores eth, stores employee info, clocks out and pays)
* No good record-keeping functionality
* Simple (and local) user-interface

## Directory Structure:
* DQPayroll.sol (solidity contract)
* index.html (user interface connected to the contact)
* main.css (formatting for index.html)
* deploy.js (deployment script of the contact)
* emp-dict.json (dicitionary of employees for mapping to fingerprint-scanner, located in ./local)
* pay-emp-info.txt (info to pass to clock-out-emp and pay-emp, located in ./local)
* node_modules, package.json and package-lock.json were created directory creation and have not been touched.
* clock-out-emp.js
* pay-emp.js
* .gitignore

## Flow (v0.0.2):
1. > testrpc
2. > deploy.js
3. Copy contract address to UI, event.js, clock-out-emp.js and pay-emp.js
4. Fund contract through metamask
5. Add employee in UI
6. Set clock UI
7. Add new employee in local clocks
8. Clock in
9. Clock out
10. Check events, contact balance and withholding balance

### Credit and resources:
* Coursetro tutorials
* solidity and web3 readthedocs
* stackoverflow
* Belisario, Alfonso (upWork teacher)

### Notes for set-up and development:

#### Dependencies:
* nodejs
* solc
* web3
* testrpc
* metamask
* python2

#### Directory Setup:
1. Navigate to your desired (new) directory
2. > npm init
3. > npm install ethereum/web3.js --save

#### Github instructions:
1. > git add .
2. > git commit -m "message"
3. > git push origin master
