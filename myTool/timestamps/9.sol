pragma solidity >=0.4.19 <0.6.0;

contract Test2 {
    function bug_time_inter(Test1 t1) public payable {
        uint256 goal_ = t1.getGoal();
        if (3000 < goal_) {
            if (now % 15 == 0) {
                goal_ = 1000;
            }
        }
    }
}

contract Test1 {
    //    uint256 public goal = 5000;

    function getGoal() public pure returns (uint256) {
        return 5000;
    }
}
