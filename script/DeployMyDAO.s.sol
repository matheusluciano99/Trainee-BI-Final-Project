// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Script, console} from "../lib/forge-std/src/Script.sol";
import {TokenDAO} from "../src/TokenDAO.sol";
import {DAO} from "../src/MyDAO.sol";

contract DeployDAO is Script {
    uint256 public constant INITIAL_SUPPLY = 10000 ether;

    function run() external returns (TokenDAO, DAO) {
        // iniciate the broadcast
        vm.startBroadcast(msg.sender); // msg.sender is the deployer

        // Deploying TokenDAO
        TokenDAO token = new TokenDAO(INITIAL_SUPPLY);
        console.log("TokenDAO deployed at:", address(token));

        // Deploying DAO with TokenDAO address
        DAO dao = new DAO(address(token));
        console.log("DAO deployed at:", address(dao));

        // end the broadcast
        vm.stopBroadcast();

        return (token, dao);
    }
}
