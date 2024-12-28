from web3 import Web3
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configurações
RPC_URL = os.getenv("RPC_URL")
DAO_ADDRESS = os.getenv("DAO_ADDRESS")
TOKEN_ADDRESS = os.getenv("TOKEN_ADDRESS")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Conexão com o nó
web3 = Web3(Web3.HTTPProvider(RPC_URL))
if not web3.is_connected():
    raise Exception("Failed to connect to the blockchain.")

class AppState:
    @staticmethod
    def connect_wallet_js():
        return """
        {   
            if (typeof window.ethereum === 'undefined') {
                alert("MetaMask não encontrada. Verifique se está instalada e habilitada em seu navegador.");
                return;
            }
            
            // Método que dispara o pop-up de conexão
            window.ethereum.request({
                method: 'wallet_requestPermissions',
                params: [{ eth_accounts: {} }]
            })
            .then(() => {
                // Agora que a permissão foi concedida, chamamos 'eth_requestAccounts'
                return window.ethereum.request({ method: 'eth_requestAccounts' });
            })
            .then(accounts => {
                const connectBtn = document.getElementById('connect-wallet');
                const disconnectBtn = document.getElementById('disconnect-wallet');
                const walletSpan = document.getElementById('wallet-address');

                if (accounts && accounts.length > 0) {
                const address = accounts[0];
                if (walletSpan && connectBtn && disconnectBtn) {
                    walletSpan.textContent = address;
                    walletSpan.style.display = 'inline-block';
                    connectBtn.style.display = 'none';
                    disconnectBtn.style.display = 'inline-block';
                    
                    // Salvar localmente (opcional)
                    localStorage.setItem('connectedWallet', address);
                }
                }
            })
            .catch(error => {
                console.error("Erro ao conectar a carteira:", error);
            });
        }"""

    @staticmethod
    def disconnect_wallet_js():
        return """
        {
            if (typeof window.ethereum === 'undefined') {
                alert("MetaMask não encontrada. Verifique se está instalada e habilitada em seu navegador.");
                return;
            }
            window.ethereum.request({
                method: 'eth_requestAccounts',
                params: [{ eth_accounts: {} }]
            })
            .then(() => {
                const walletSpan = document.getElementById('wallet-address');
                if (walletSpan) {
                    walletSpan.textContent = '';
                    walletSpan.style.display = 'none';
                }
                localStorage.removeItem('connectedWallet'); // Remove do localStorage
                document.getElementById('connect-wallet').style.display = 'inline-block'; // Mostra conectar
                document.getElementById('disconnect-wallet').style.display = 'none'; // Esconde desconectar
            })
            .catch(err => {
                console.error("Erro ao desconectar a carteira:", err);
            });
        }"""


# Função para carregar a ABI a partir do arquivo JSON
def load_abi(contract_name:str):
    abi_path = os.path.join("../out", contract_name, f"{contract_name.strip('.sol')}.json")
    if not os.path.exists(abi_path):
        raise FileNotFoundError(f"ABI não encontrada para {contract_name} em {abi_path}.")
    with open(abi_path, 'r') as f:
        artifact = json.load(f)
        if "abi" not in artifact:
            raise KeyError(f"'abi' não encontrado no arquivo {abi_path}.")
        return artifact["abi"]

# Endereços e ABI dos contratos
dao_abi = load_abi("DAO.sol")
token_abi = load_abi("TokenDAO.sol")

# Instância dos contratos
dao_contract = web3.eth.contract(address=DAO_ADDRESS, abi=dao_abi)
token_contract = web3.eth.contract(address=TOKEN_ADDRESS, abi=token_abi)
    
# Funções de interação com os contratos

def create_proposal(title, description, voting_period, sender_address):
    nonce = web3.eth.get_transaction_count(sender_address)
    tx = dao_contract.functions.createProposal(
        title, description, voting_period
    ).buildTransaction({
        'from': sender_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('20', 'gwei'),
    })
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt

def vote(proposal_id, support, sender_address):
    """Registra um voto em uma proposta."""
    nonce = web3.eth.get_transaction_count(sender_address)
    tx = dao_contract.functions.vote(proposal_id, support).build_transaction({
        'from': sender_address,
        'nonce': nonce,
        'gas': 2000000,
        'gasPrice': web3.to_wei('20', 'gwei')
    })
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt


def execute_proposal(proposal_id, sender_address):
    """Executa uma proposta caso os critérios sejam atingidos."""
    nonce = web3.eth.get_transaction_count(sender_address)
    tx = dao_contract.functions.executeProposal(proposal_id).build_transaction({
        'from': sender_address,
        'nonce': nonce,
        'gas': 3000000,
        'gasPrice': web3.to_wei('20', 'gwei')
    })
    signed_tx = web3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    receipt = web3.eth.wait_for_transaction_receipt(tx_hash)
    return receipt


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

