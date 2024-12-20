// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract TokenDAO is ERC20 {
    constructor(uint256 initialSupply) ERC20("Blockchain Insper", "BCI") {
        _mint(msg.sender, initialSupply);
    }
}
