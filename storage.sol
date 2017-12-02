pragma solidity ^0.4.16;

contract Owned {
    address public owner;

    function Owned() {
        owner = msg.sender;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function transferOwnership(address newOwner) public onlyOwner {
        owner = newOwner;
    }

    function getOwner() public constant returns (address) {
        return owner;
    }
}

contract FileHashStorage is Owned {
    struct File {
        string name;
        uint uploadDate;
        uint size;
    }
    mapping(string => File) private files;
    mapping(string => string[]) private fileOwners;
    string[] public owners;
    uint public ownerID = 0;

    /*
    owners = ["Jung", "Park", ...]
    fileOwners["Jung"] = ["0xABCD1234", "0xDEAD4321"] // Hashed file
    files["0xABCD1234"] = {
      name: "test_file.pdf",
      registerDate: 17203124, // Unix timestamp
      size: 154000 // Bytes
    }
    */

    event Upload(string personName, string fileHash, File file);


    function upload(string personName, string fileHash, string fileName, uint fileSize) onlyOwner public {
        ownerID++;
        owners.push(personName);
        File memory f = File(fileName, now, fileSize);
        files[fileHash] = f;
        Upload(personName, fileHash, f);
    }

    function checkExist(string fileHash) onlyOwner public view returns (bool) {
        if (files[fileHash].size > 0) {
            return true;
        }
        return false;
    }

    function getOwnerName(uint id) onlyOwner public view returns (string) {
        return owners[id];
    }

    function getFileInfo(string fileHash) onlyOwner public view returns (string, uint, uint) {
        return (files[fileHash].name, files[fileHash].uploadDate, files[fileHash].size);
    }
}
