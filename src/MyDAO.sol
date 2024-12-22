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
        mapping(address => bool) hasVoted; // To prevent multiple voting
    }

    uint256 public proposalCount;
    mapping(uint256 => Proposal) private proposals;
    TokenDAO public token;

    event ProposalCreated(
        uint256 indexed proposalId,
        string title,
        string description,
        uint256 endTime,
        address indexed proposer
    );

    event VoteCast(
        uint256 indexed proposalId,
        address indexed voter,
        bool support,
        uint256 weight
    );

    event ProposalExecuted(uint256 indexed proposalId);

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

        Proposal storage newProposal = proposals[proposalCount];
        newProposal.title = title;
        newProposal.description = description;
        newProposal.endTime = endTime;
        newProposal.forVotes = 0;
        newProposal.againstVotes = 0;
        newProposal.executed = false;
        newProposal.proposer = msg.sender;

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
        require(
            proposalId > 0 && proposalId <= proposalCount,
            "Proposal does not exist"
        );
        Proposal storage proposal = proposals[proposalId];
        require(proposal.endTime > block.timestamp, "Voting period has ended");
        require(!proposal.executed, "Proposal already executed");
        require(!proposal.hasVoted[msg.sender], "Already voted");
        require(
            token.balanceOf(msg.sender) >= 1 ether,
            "Insufficient tokens to vote"
        );

        uint256 voterTokens = token.balanceOf(msg.sender);

        proposal.hasVoted[msg.sender] = true;

        if (support) {
            proposal.forVotes += voterTokens;
        } else {
            proposal.againstVotes += voterTokens;
        }

        emit VoteCast(proposalId, msg.sender, support, voterTokens);
    }

    function executeProposal(uint256 proposalId) external {
        require(
            proposalId > 0 && proposalId <= proposalCount,
            "Proposal does not exist"
        );
        Proposal storage proposal = proposals[proposalId];
        proposal.executed = true;

        emit ProposalExecuted(proposalId);
    }

    function getProposal(
        uint256 proposalId
    )
        external
        view
        returns (
            string memory,
            string memory,
            uint256,
            uint256,
            uint256,
            bool,
            address
        )
    {
        Proposal storage proposal = proposals[proposalId];
        return (
            proposal.title,
            proposal.description,
            proposal.endTime,
            proposal.forVotes,
            proposal.againstVotes,
            proposal.executed,
            proposal.proposer
        );
    }
}
