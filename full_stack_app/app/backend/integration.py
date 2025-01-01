import reflex as rx
from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Settings
RPC_URL = os.getenv("RPC_URL")
DAO_ADDRESS = os.getenv("DAO_ADDRESS")
TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Conection to the blockchain
web3 = Web3(Web3.HTTPProvider(RPC_URL))
if not web3.is_connected():
    raise Exception("Failed to connect to the blockchain.")

# function to load the ABI of a contract
def load_abi(contract_name:str):
    abi_path = os.path.join("../out", contract_name, f"{contract_name.strip('.sol')}.json")
    if not os.path.exists(abi_path):
        raise FileNotFoundError(f"ABI não encontrada para {contract_name} em {abi_path}.")
    with open(abi_path, 'r') as f:
        artifact = json.load(f)
        if "abi" not in artifact:
            raise KeyError(f"'abi' não encontrado no arquivo {abi_path}.")
        return artifact["abi"]

# Contract ABIs
dao_abi = load_abi("DAO.sol")
token_abi = load_abi("TokenDAO.sol")

# Contract instances
dao_contract = web3.eth.contract(address=DAO_ADDRESS, abi=dao_abi)
token_contract = web3.eth.contract(address=TOKEN_ADDRESS, abi=token_abi)
    
# Funções de interação com os contratos
def create_proposal(title, description, voting_period, sender_address):
    """Create a proposal on the DAO."""
    try:
        # First create proposal on blockchain
        nonce = web3.eth.get_transaction_count(Web3.to_checksum_address(sender_address))
        tx = dao_contract.functions.createProposal(
            title, description, voting_period
        ).build_transaction({
            'from': Web3.to_checksum_address(sender_address),
            'nonce': nonce,
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei'),
        })
        
        return tx
    
    except Exception as e:
        raise Exception(f"Failed to create the proposal. {str(e)}")

def vote(proposal_id, support, sender_address):
    """Cast a vote on a proposal."""
    try:
        # Execute blockchain transaction
        nonce = web3.eth.get_transaction_count(Web3.to_checksum_address(sender_address))
        tx = dao_contract.functions.castVote(proposal_id, support).build_transaction({
            'from': Web3.to_checksum_address(sender_address),
            'nonce': nonce,
            'gas': 2000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })

        return tx
    
    except Exception as e:
        return rx.window_alert(f"Error casting vote: {str(e)}")


def execute_proposal(proposal_id, sender_address):
    """Execeute a proposal."""
    try:
        nonce = web3.eth.get_transaction_count(Web3.to_checksum_address(sender_address))
        tx = dao_contract.functions.executeProposal(proposal_id).build_transaction({
            'from': Web3.to_checksum_address(sender_address),
            'nonce': nonce,
            'gas': 3000000,
            'gasPrice': web3.to_wei('20', 'gwei')
        })
    
        return tx
    
    except Exception as e:
        return rx.window_alert(f"Error executing proposal: {str(e)}")


def get_proposal(proposal_id):
    """Get proposal details."""
    return dao_contract.functions.getProposal(proposal_id).call()

def list_proposals():
    """List all proposals."""
    proposal_count = dao_contract.functions.proposalCount().call()
    proposals = []
    for i in range(1, proposal_count + 1):
        p = dao_contract.functions.getProposal(i).call()
        proposals.append({
            "id": i,
            "title": p[0],
            "description": p[1],
            "endTime": p[2],
            "forVotes": p[3],
            "againstVotes": p[4],
            "executed": p[5],
            "proposer": p[6],
        })
    return proposals

