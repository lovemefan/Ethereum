pragma solidity >=0.4.22 <0.6.0;

contract Corpus {

    struct Key {
        string encryKey;
        bool isUsed;
    }


    struct FileKeys {
        bool isUsed;
        uint size;
        mapping(string => Key) data;
    }

    struct AddressFiles {
        uint size;
        mapping(address => FileKeys)  data;
    }


    AddressFiles addressFiles;

    address  minter;

    mapping(address => uint) public balances;

    event Send(address from, address to, uint amount);

    constructor() public{
        // init total number of corpus and support mine
        minter = msg.sender;
        balances[msg.sender] = 10000;
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



    function getFileKey(address receiver, string memory file_name) public view returns(string){
        // only read your own files
        // require(msg.sender == receiver, "you can only request for yourself");
        require(addressFiles.data[receiver].isUsed, "address is empty");
        require(addressFiles.data[receiver].data[file_name].isUsed, "file_name is not exist in block");
        string storage encry_key = addressFiles.data[receiver].data[file_name].encryKey;

        return encry_key;
    }

    function insertFileKey(address receiver, string memory file_name, string memory encry_key) public  returns(string success){
        // only read your own files
        // require(msg.sender == receiver, "you can only request for yourself");


        if (addressFiles.data[receiver].isUsed) {
            addressFiles.data[receiver].isUsed = true;
            addressFiles.data[receiver].size++;
            addressFiles.data[receiver].data[file_name] = Key(encry_key, true);

        }else {
            // address not init
            addressFiles.size++;
            addressFiles.data[receiver] = FileKeys(true, 1);
            addressFiles.data[receiver].size++;
            addressFiles.data[receiver].data[file_name] = Key(encry_key, true);

        }

        return  addressFiles.data[receiver].data[file_name].encryKey;
    }

}
