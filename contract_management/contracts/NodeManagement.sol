contract NodeManagement {

  address public owner;
  address[] members;
  bytes[] public transactions;

  modifier isOwner {
    if (msg.sender == owner) _
  }

  modifier isMember {
    for (uint i = 0; i < members.length; i++) {
      if (msg.sender == members[i]) _
    }
  }

  event NewTransaction(uint id);
  event Message(address indexed recipient, bytes message);
 
  function NodeManagement() {
    // constructor
    owner = msg.sender;
  }
  
  function send(address recipient, bytes message) {
    Message(recipient, message);
  }

  function addMember(address member) isOwner {
    members[members.length++] = member;
  }

  function removeMember(address member) isOwner {
    for (uint i = 0; i < members.length; i++) {
      if (member == members[i]) {
        delete members[i];
      }
    }
  }

  function getMembers() isOwner constant returns (address[]) {
    return members;
  }

  function addTransaction(bytes transaction) isMember {
    uint id = transactions.length++;
    transactions[id] = transaction;
    NewTransaction(id);
  }

  function numTransactions() constant returns (uint) {
    return transactions.length;
  }

}
