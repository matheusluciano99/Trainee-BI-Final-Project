import reflex as rx
from .integration import create_proposal, list_proposals, vote
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
        if not self.title or not self.description or self.voting_period <= 0:
            return
        
        try:
            sender_address = print(WalletState.address)

            async with self:
                create_proposal(
                    self.title,
                    self.description, 
                    self.voting_period,
                    sender_address
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
        try:
            sender_address = "0xf39fd6e51aad88f6f4ce6ab8827279cfffb92266"
            async with self:
                vote(
                    proposal_id, 
                    support, 
                    sender_address
                )
            
            return rx.window_alert("Vote submitted successfully!")
        except Exception as e:
            return rx.window_alert(f"Error voting: {str(e)}")