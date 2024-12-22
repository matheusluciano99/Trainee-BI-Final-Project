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
    address public USER3 = makeAddr("user3"); // User without tokens
    uint256 public constant INITIAL_SUPPLY = 10000 ether;
    uint256 public constant AIRDROP = 10 ether;

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

        // Distribute tokens to users
        token.transfer(USER, AIRDROP);
        token.transfer(USER2, 2 * AIRDROP);

        // Approve the DAO to spend user tokens
        vm.prank(USER);
        token.approve(address(dao), AIRDROP);

        vm.prank(USER2);
        token.approve(address(dao), 2 * AIRDROP);
    }

    /* ------- BEGINNING CREATE PROPOSAL TESTS ------- */
    function testUserCanCreateProposal() public {
        // User creates a proposal
        string memory title = "Proposal by USER";
        string memory description = "This is a proposal from USER";
        uint256 votingPeriod = 1 days;

        vm.prank(USER);
        uint256 proposalId = dao.createProposal(
            title,
            description,
            votingPeriod
        );

        // Verify if the data was stored correctly
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
        vm.prank(USER3);
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
    /* ------- ENDING CREATE PROPOSAL TESTS ------- */

    /* ------- BEGINNING CAST VOTE TESTS ------- */

    function testUserCanVoteForProposal() public {
        string memory title = "Test Proposal";
        string memory description = "This is a test";
        uint256 votingPeriod = 1 days;

        uint256 proposalId = dao.createProposal(
            title,
            description,
            votingPeriod
        );

        // Usuário vota a favor
        vm.prank(USER);
        dao.castVote(proposalId, true);

        // Verificar os votos a favor
        (, , , uint256 forVotes, uint256 againstVotes, , ) = dao.proposals(
            proposalId
        );
        assertEq(forVotes, AIRDROP, "For votes are incorrect");
        assertEq(againstVotes, 0, "Against votes should be zero");
    }

    function testUserCanVoteAgainstProposal() public {
        string memory title = "Proposal Against Voting";
        string memory description = "Description for voting";
        uint256 votingPeriod = 1 days;

        // Criar uma proposta
        vm.prank(USER);
        uint256 proposalId = dao.createProposal(
            title,
            description,
            votingPeriod
        );

        // Usuário vota contra
        vm.prank(USER2);
        dao.castVote(proposalId, false);

        // Verificar os votos contra
        (, , , uint256 forVotes, uint256 againstVotes, , ) = dao.proposals(
            proposalId
        );
        assertEq(forVotes, 0, "For votes should be zero");
        assertEq(againstVotes, 2 * AIRDROP, "Against votes are incorrect");
    }

    function testCannotVoteAfterVotingPeriodEnds() public {
        string memory title = "Expired Proposal";
        string memory description = "Description for expired proposal";
        uint256 votingPeriod = 1 days;

        // Criar uma proposta
        vm.prank(USER);
        uint256 proposalId = dao.createProposal(
            title,
            description,
            votingPeriod
        );

        // Avançar o tempo para além do período de votação
        vm.warp(block.timestamp + 2 days);

        // Tentar votar após o período
        vm.prank(USER);
        vm.expectRevert("Voting period has ended");
        dao.castVote(proposalId, true);
    }

    function testCannotVoteWithoutSufficientTokens() public {
        string memory title = "Proposal with Insufficient Tokens";
        string memory description = "Description for insufficient tokens";
        uint256 votingPeriod = 1 days;

        // Criar uma proposta
        vm.prank(USER);
        uint256 proposalId = dao.createProposal(
            title,
            description,
            votingPeriod
        );

        // Usuário sem tokens tenta votar
        vm.prank(USER3);
        vm.expectRevert("Insufficient tokens to vote");
        dao.castVote(proposalId, true);
    }

    function testCannotVoteOnNonExistentProposal() public {
        uint256 invalidProposalId = 999;

        // Tentar votar em uma proposta inexistente
        vm.prank(USER);
        vm.expectRevert("Proposal does not exist");
        dao.castVote(invalidProposalId, true);
    }

    function testCannotVoteOnExecutedProposal() public {
        string memory title = "Executed Proposal";
        string memory description = "Description for executed proposal";
        uint256 votingPeriod = 1 days;

        // Criar uma proposta
        vm.prank(USER);
        uint256 proposalId = dao.createProposal(
            title,
            description,
            votingPeriod
        );

        // Simular a execução da proposta
        vm.prank(USER);
        dao.executeProposal(proposalId);

        // Tentar votar após execução
        vm.prank(USER);
        vm.expectRevert("Proposal already executed");
        dao.castVote(proposalId, true);
    }

    /* ------- ENDING CAST VOTE TESTS ------- */
}
