// SPDX-License-Identifier: MIT
pragma solidity ^0.8.13;

import {TokenDAO} from "./TokenDAO.sol";

contract DAO {
    struct Proposal {
        string title;
        string description;
        uint256 endTime;
        uint256 forVotes;
        uint256 againstVotes;
        bool executed;
        address proposer;
    }

    uint256 public proposalCount;
    mapping(uint256 => Proposal) public proposals;
    TokenDAO public token;

    event ProposalCreated(
        uint256 proposalId,
        string title,
        string description,
        uint256 endTime,
        address proposer
    );

    constructor(address _tokenAddress) {
        require(_tokenAddress != address(0), "Invalid token address");
        token = TokenDAO(_tokenAddress);
    }

    function createProposal(
        string memory title,
        string memory description,
        uint256 votingPeriod
    ) external returns (uint256 proposalId) {
        require(votingPeriod > 0, "Invalid voting period");
        require(token.balanceOf(msg.sender) >= 1 ether, "Insufficient tokens");

        proposalCount++;

        uint256 endTime = block.timestamp + votingPeriod;

        proposals[proposalCount] = Proposal({
            title: title,
            description: description,
            endTime: endTime,
            forVotes: 0,
            againstVotes: 0,
            executed: false,
            proposer: msg.sender
        });

        emit ProposalCreated(
            proposalCount,
            title,
            description,
            endTime,
            msg.sender
        );

        return proposalCount;
    }

    function castVote(uint256 proposalId, bool support) external {
        // TODO: Implement
    }

    function executeProposal(uint256 proposalId) external {
        // TODO: Implement
    }

    function getProposal(
        uint256 proposalId
    ) external view returns (Proposal memory) {
        // TODO: Implement
    }
}
