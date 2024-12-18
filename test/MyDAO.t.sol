// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "forge-std/Test.sol";
import {DAO} from "../src/MyDAO.sol";

contract DAOTest is Test {
    DAO dao;

    // Event to be used in the test
    event ProposalCreated(
        uint256 proposalId,
        string title,
        string description,
        uint256 endTime,
        address proposer
    );

    function setUp() public {
        dao = new DAO();
    }

    function testCreateProposalIncrementsProposalCount() public {
        uint256 initialProposalCount = dao.proposalCount();
        dao.createProposal("Test Proposal", "This is a test", 1 days);
        uint256 finalProposalCount = dao.proposalCount();
        assertEq(
            finalProposalCount,
            initialProposalCount + 1,
            "Proposal count should increment by 1"
        );
    }

    function testCreateProposalStoresCorrectData() public {
        string memory title = "Test Proposal";
        string memory description = "This is a test";
        uint256 votingPeriod = 2 days;

        uint256 proposalId = dao.createProposal(
            title,
            description,
            votingPeriod
        );
        (
            string memory storedTitle,
            string memory storedDescription,
            uint256 storedEndTime,
            ,
            ,
            ,
            address proposer
        ) = dao.proposals(proposalId);

        assertEq(storedTitle, title, "Proposal title is incorrect");
        assertEq(
            storedDescription,
            description,
            "Proposal description is incorrect"
        );
        assertEq(
            storedEndTime,
            block.timestamp + votingPeriod,
            "Proposal endTime is incorrect"
        );
        assertEq(proposer, address(this), "Proposer address is incorrect");
    }

    function testCreateProposalEmitsEvent() public {
        string memory title = "Test Proposal";
        string memory description = "This is a test";
        uint256 votingPeriod = 1 days;

        vm.expectEmit(true, true, true, true);
        emit ProposalCreated(
            1,
            title,
            description,
            block.timestamp + votingPeriod,
            address(this)
        );
        dao.createProposal(title, description, votingPeriod);
    }

    function testCantCreateProposalWithZeroVotingPeriod() public {
        string memory title = "Test Proposal";
        string memory description = "This is a test";

        vm.expectRevert("Invalid voting period");
        dao.createProposal(title, description, 0);
    }
}
