// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console} from "../lib/forge-std/src/Test.sol";
import {DAO} from "../src/MyDAO.sol";
import {TokenDAO} from "../src/TokenDAO.sol";

contract DAOTest is Test {
    DAO dao;
    TokenDAO token;

    address public USER = makeAddr("user");
    address public USER2 = makeAddr("user2");
    uint256 public constant INITIAL_SUPPLY = 10000 ether;

    // Event to be used in the test
    event ProposalCreated(
        uint256 proposalId,
        string title,
        string description,
        uint256 endTime,
        address proposer
    );

    function setUp() public {
        token = new TokenDAO(INITIAL_SUPPLY);
        dao = new DAO(address(token));

        // Distribuir tokens para os usuários
        token.transfer(USER, 10 ether);

        // Aprovar o DAO para gastar tokens do usuário
        vm.prank(USER);
        token.approve(address(dao), 10 ether);
    }

    function testUserCanCreateProposal() public {
        // Usuário cria uma proposta
        string memory title = "Proposal by USER";
        string memory description = "This is a proposal from USER";
        uint256 votingPeriod = 1 days;

        vm.prank(USER);
        uint256 proposalId = dao.createProposal(
            title,
            description,
            votingPeriod
        );

        // Verificar se os dados foram armazenados corretamente
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
        assertEq(proposer, USER, "Proposer address is incorrect");
    }

    function testUserCantCreateProposalWithoutTokens() public {
        vm.expectRevert("Insufficient tokens");
        vm.prank(USER2);
        dao.createProposal("Test Proposal", "This is a test", 1 days);
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
