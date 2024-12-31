import reflex as rx
import json
from web3 import Web3
from web3.main import HexBytes
from .integration import create_proposal, list_proposals, vote, execute_proposal
from .wallet_state import WalletState
from typing import List, Dict, Any

class ProposalState(rx.State):
    title: str = ""
    description: str = ""
    voting_period: int = 0
    show_form: bool = False
    proposals: List[Dict[str, Any]] = list_proposals if isinstance(list_proposals, list) else []

    @rx.event(background=True)
    async def send_transaction(self, tx_dict):
        # Send transaction through MetaMask
        return rx.call_script(f"""{{
            async function sendTransaction() {{
                try {{
                    const tx = {json.dumps(tx_dict)};
                    await window.ethereum.request({{
                        method: 'eth_sendTransaction',
                        params: [tx]
                    }});
                    window.location.reload();
                }} catch (err) {{
                    console.error(err);
                    alert('Transaction failed: ' + (err.message || err));
                }}
            }}
            sendTransaction();
        }}""")
        

    @rx.event
    async def get_proposals(self):
        """Update proposals list."""
        self.proposals = list_proposals() 

    
    @rx.event(background=True)
    async def create_new_proposal(self):
        
        async with self:
            wallet_state = await self.get_state(WalletState)

            if not self.title or not self.description or self.voting_period <= 0:
                return rx.window_alert("Please fill all fields!")
                
            if not wallet_state.is_connected:
                return rx.window_alert("Please connect your wallet!")

        
        try:
            async with self:
                tx = create_proposal(
                    self.title,
                    self.description, 
                    self.voting_period,
                    wallet_state.address
                )

                # Converta a transação para um dicionário primeiro
                tx_dict = {
                    'from': tx['from'],
                    'to': tx.get('to'),
                    'data': tx.get('data'),
                    'gas': hex(int(tx['gas'])),
                    'gasPrice': hex(int(tx['gasPrice'])),
                    'nonce': hex(tx['nonce']),
                    'chainId': tx.get('chainId'),
                    'value': tx.get('value')
                }

                # Reset form
                self.show_form = False

                # Convert proposals to plain dictionaries before setting state
                self.proposals = list_proposals()

            # Send transaction
            return ProposalState.send_transaction(tx_dict)
        
        except Exception as e:
            return rx.window_alert(f"Error creating proposal: {str(e)}")
        
    @rx.event(background=True)
    async def vote_on_proposal(self, proposal_id: int, support: bool):
        """Handle voting through state management."""

        async with self:
            wallet_state = await self.get_state(WalletState)
                
            if not wallet_state.is_connected:
                return rx.window_alert("Please connect your wallet!")

        try:
            async with self:
                tx = vote(
                    proposal_id, 
                    support, 
                    wallet_state.address
                )

                # Converta a transação para um dicionário primeiro
                tx_dict = {
                    'from': tx['from'],
                    'to': tx.get('to'),
                    'data': tx.get('data'),
                    'gas': hex(int(tx['gas'])),
                    'gasPrice': hex(int(tx['gasPrice'])),
                    'nonce': hex(tx['nonce']),
                    'chainId': tx.get('chainId'),
                    'value': tx.get('value')
                }

            # Send transaction
            return ProposalState.send_transaction(tx_dict)
        except Exception as e:
            return rx.window_alert(f"Error voting: {str(e)}")
        
    @rx.event(background=True)
    async def execute_proposal(self, proposal_id: int):
        """Execute proposal with wallet check."""
        async with self:
            wallet_state = await self.get_state(WalletState)
                
            if not wallet_state.is_connected:
                return rx.window_alert("Please connect your wallet!")

        try:
            async with self:
                tx = execute_proposal(proposal_id, wallet_state.address)

                # Converta a transação para um dicionário primeiro
                tx_dict = {
                    'from': tx['from'],
                    'to': tx.get('to'),
                    'data': tx.get('data'),
                    'gas': hex(int(tx['gas'])),
                    'gasPrice': hex(int(tx['gasPrice'])),
                    'nonce': hex(tx['nonce']),
                    'chainId': tx.get('chainId'),
                    'value': tx.get('value')
                }

                self.proposals = list_proposals()

            # Send transaction
            return ProposalState.send_transaction(tx_dict)
        except Exception as e:
            return rx.window_alert(f"Error executing proposal: {str(e)}")
        

    def toggle_form(self):
        self.show_form = not self.show_form