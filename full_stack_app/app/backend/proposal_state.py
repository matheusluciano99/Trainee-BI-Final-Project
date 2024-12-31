import reflex as rx
from .integration import create_proposal, list_proposals, vote, execute_proposal
from .wallet_state import WalletState
from typing import List, Dict

class ProposalState(rx.State):
    title: str = ""
    description: str = ""
    voting_period: int = 0
    show_form: bool = False
    proposals: List[Dict[str, str]] = list_proposals if isinstance(list_proposals, list) else []


    @rx.event
    async def get_proposals(self):
        """Update proposals list."""
        self.proposals = list_proposals() 
        

    def toggle_form(self):
        self.show_form = not self.show_form

    
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
                wallet_state = await self.get_state(WalletState)
                create_proposal(
                    self.title,
                    self.description, 
                    self.voting_period,
                    wallet_state.address
                )
                # Reset form
                self.title = ""
                self.description = ""
                self.voting_period = 0
                self.show_form = False

                # Convert proposals to plain dictionaries before setting state
                self.proposals = list_proposals()
            

            return rx.window_alert("Proposal created successfully!")
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
                wallet_state = await self.get_state(WalletState)
                vote(
                    proposal_id, 
                    support, 
                    wallet_state.address
                )
            
            return rx.window_alert("Vote submitted successfully!")
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
                wallet_state = self.get_state(WalletState)
                execute_proposal(proposal_id, wallet_state.address)
                self.proposals = list_proposals()
            return rx.window_alert("Proposal executed successfully!")
        except Exception as e:
            return rx.window_alert(f"Error executing proposal: {str(e)}")