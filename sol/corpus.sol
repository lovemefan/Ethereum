pragma solidity >=0.4.22 <0.6.0;

contract Corpus {

    string name;
    string key;

    address  minter;
    mapping(address => uint) public balances;

    event Send(address from, address to, uint amount);

    constructor(uint initalSupply)public{
        // init total number of corpus and support mine
        minter = msg.sender;
        balances[msg.sender] = initalSupply;
    }

    function getName() public view returns(string memory name) {
        return name;
    }

    function setName(string memory new_name) public  {
        name = new_name;
    }

    function getKey() public view returns(string memory key) {
        return key;
    }

    function setKey(string memory new_key) public  {
        key = new_key;
    }

    function mint(address receiver, uint amount)public{
        require(msg.sender == minter);
        balances[receiver] += amount;
    }

    function transfer(address receiver, uint amount)public returns(bool success){
        // check if the sender has enough
        require(balances[msg.sender] >= amount);
        // check if  overflowed
        require(balances[receiver] + amount >= balances[receiver]);
        require(balances[receiver] + amount >= amount);
        balances[msg.sender] -= amount;
        balances[receiver] += amount;
        emit Send(msg.sender, receiver, amount);
        return true;
    }

    function getBalances() public view returns(uint){
        return balances[msg.sender];
    }
}
