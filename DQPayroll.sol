pragma solidity ^0.4.17;

contract DQPayroll {

	/* Variables*/
	address public owner;
	address public wth_account;
	uint256 public wth_balance;

	struct emp_struct {
		string name; 
		uint256 wage;
		uint256 wth; // basis points (1/100th of 1%)
	}

	mapping (address => emp_struct) public emp_struct_map;
	mapping (address => bool) public clock_map;
	mapping (address => uint256) public emp_balance_map;


	/* Events*/
	event NewEmployee (address _emp_addr, string _name, uint256 _wage, uint256 _wth);
	event PayEmployee(address _emp_addr, uint256 _emp_balance, uint256 _new_wth);
	event SetClock(address _clock_addr);
	event TransOwnership(address _new_owner, address _new_wth_addr);
	event ClockOut(address _emp_addr, uint256 _time_worked);
	event PayWithholdings(address _wth_account, uint256 _wth_balance);
	

	/* Functions */
	function DQPayroll(address _wth_addr) public { // Constructor function
		owner = msg.sender; // Registering owner upon creation (see deploy.js)
		wth_account = _wth_addr; // Registering wth_account (see deploy.js)
	}
	
	function() public payable {} // Contract can accept eth 

	function transOwnership(address _new_owner, address _new_wth_addr) public onlyOwner {
		owner = _new_owner;
		wth_account = _new_wth_addr;
		emit TransOwnership(_new_owner, _new_wth_addr);
	}

	function setClock(address _clock_addr) public onlyOwner {
		clock_map[_clock_addr] = true; 
		emit SetClock(_clock_addr);
	}

	function newEmployee(address _emp_addr, string _name, uint256 _wage, uint256 _wth) public onlyOwner {
        emp_struct_map[_emp_addr] = emp_struct(_name, _wage, _wth); // Create mapping and fill struct
        emit NewEmployee(_emp_addr, _name, _wage, _wth); // Emit event
	}

	function clockOut(address _emp_addr, uint256 _time_worked) public onlyClocks {
		emp_balance_map[_emp_addr] += _time_worked * emp_struct_map[_emp_addr].wage; // Increments emp_balance_map based on _time_worked and wage
		emit ClockOut(_emp_addr, _time_worked);
	}

	function payEmployee(address _emp_addr) public { // No modifier, trasnsfers funds to emp, resets empp_balance to zero and withholds taxes
		require(address(this).balance >= emp_balance_map[_emp_addr]); // Contract has enough funds
		var new_wth = (emp_balance_map[_emp_addr] / (10000/emp_struct_map[_emp_addr].wth));
		_emp_addr.transfer(emp_balance_map[_emp_addr] - new_wth ); // Transfer to employee
		wth_balance += new_wth;
		emit PayEmployee(_emp_addr, emp_balance_map[_emp_addr], new_wth); // Should also emit transaction here
		emp_balance_map[_emp_addr] = 0; // Set emp_balance_map back to zero 
		}

	function payWithholdings() public onlyOwner {
		require(address(this).balance >= wth_balance);
		wth_account.transfer(wth_balance);
		emit PayWithholdings(wth_account, wth_balance);
		wth_balance = 0;
	}

	function kill() public onlyOwner {
		selfdestruct(owner);
	}


	/* Modifiers */
	modifier onlyOwner {
		require(msg.sender == owner);
        _;
	}

	modifier onlyClocks {
		require(clock_map[msg.sender]);
		_;
	}
}