pragma solidity >=0.4.19 <0.6.0;

contract Test2 {
    function bug_time_inter(Test1 t1) public payable {
        uint256 goal_ = t1.getGoal();
        uint256 time = now;
        if (3000 < goal_) {
            if (goal_ % 15 == 0) {
                msg.sender.transfer(time);
            }
        }
    }
}

contract Test1 {
    uint256 public goal = 5000;

    function getGoal() public view returns (uint256) {
        return goal;
    }
}
