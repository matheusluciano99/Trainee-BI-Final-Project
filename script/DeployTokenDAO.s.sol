// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {Script} from "../lib/forge-std/src/Script.sol";
import {TokenDAO} from "../src/TokenDAO.sol";

contract DeployTokenDAO is Script {
    uint256 public constant INITIAL_SUPPLY = 10000 ether;

    function run() external {
        vm.startBroadcast();
        new TokenDAO(INITIAL_SUPPLY);
        vm.stopBroadcast();
    }
}
