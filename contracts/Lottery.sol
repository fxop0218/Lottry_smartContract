// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol"; // import a interface (similar to java)
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";

//import "./VRFConsumerBaseV2.sol";
//import "./VRFCoordinatorV2Interface.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    address payable public recentWinner;
    uint256 randomness;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    //0 OPEN
    //1 CLOSED
    //2 CALCULATING_WINNER

    LOTTERY_STATE public lottery_state;

    uint256 public fee;
    bytes32 public keyhash;

    constructor(
        address _priceFeedAddress,
        address _vrfCordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) VRFConsumerBase(_vrfCordinator, _link) {
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED; //1
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        //50$ min
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(msg.value >= getEntraceFee());
        players.push(payable(msg.sender));
    }

    function getEntraceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustPrice = uint256(price) * 10**10;
        // 50$/2.000$
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustPrice;
        return costToEnter;
    }

    function startLottery() public {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "The lottery is closed now"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    // Get random winner
    function endLottery() public onlyOwner {
        // !!! DON'T USE IN REAL PRODUCTION CASE
        /* uint256(
            keccak256(
                abi.encodePacked(
                    nonce, // predictable
                    msg.sender, // predictable
                    block.difficulty, // can be manipulated
                    block.timestamp // predictable
                )
            )
        ) % players.length; */
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomless)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "You arem't there yet"
        );
        require(_randomless > 0, "random-not-found");
        uint256 indexOfWinner = _randomless % players.length;
        recentWinner = players[indexOfWinner];
        recentWinner.transfer(address(this).balance);
        // reset the game
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomless;
    }
}
