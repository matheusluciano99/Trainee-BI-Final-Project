from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações
RPC_URL = os.getenv("RPC_URL")
DAO_ADDRESS = os.getenv("DAO_CONTRACT_ADDRESS")
TOKEN_ADDRESS = os.getenv("TOKEN_CONTRACT_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Conexão com o nó
web3 = Web3(Web3.HTTPProvider(RPC_URL))
if not web3.is_connected():
    raise Exception("Failed to connect to the blockchain.")

# Endereços e ABI dos contratos
dao_abi = [...]  # ABI do contrato DAO
token_abi = [...]  # ABI do contrato TokenDAO

# Instância dos contratos
dao_contract = web3.eth.contract(address=DAO_ADDRESS, abi=dao_abi)
token_contract = web3.eth.contract(address=TOKEN_ADDRESS, abi=token_abi)
    
# Funções de interação com os contratos

def create_proposal(title, description, voting_period, sender_address):
    tx = dao_contract.functions.createProposal(
        title, description, voting_period
    ).buildTransaction({
        'from': sender_address,
        'nonce': web3.eth.getTransactionCount(sender_address),
        'gas': 2000000,
        'gasPrice': web3.toWei('20', 'gwei'),
    })
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return web3.toHex(tx_hash)

def vote(proposal_id, support, sender_address):
    tx = dao_contract.functions.castVote(proposal_id, support).buildTransaction({
        'from': sender_address,
        'nonce': web3.eth.getTransactionCount(sender_address),
        'gas': 2000000,
        'gasPrice': web3.toWei('20', 'gwei'),
    })
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return web3.toHex(tx_hash)

def execute_proposal(proposal_id, sender_address):
    tx = dao_contract.functions.executeProposal(proposal_id).buildTransaction({
        'from': sender_address,
        'nonce': web3.eth.getTransactionCount(sender_address),
        'gas': 2000000,
        'gasPrice': web3.toWei('20', 'gwei'),
    })
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    return web3.toHex(tx_hash)

def get_proposal(proposal_id):
    return dao_contract.functions.getProposal(proposal_id).call()

def list_proposals():
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

