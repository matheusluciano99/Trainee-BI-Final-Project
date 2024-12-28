import reflex as rx
from .integration import create_proposal

class ProposalFormState(rx.State):
    title: str = ""
    description: str = ""
    voting_period: int = 0
    show_form: bool = False

    def toggle_form(self):
        self.show_form = not self.show_form

    def create_new_proposal(self):
        if not self.title or not self.description or self.voting_period <= 0:
            return
        
        try:
            # Hardcoded sender for testing - in production get from connected wallet
            sender_address = "YOUR_ADDRESS_HERE"
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
            return rx.window_alert("Proposal created successfully!")
        except Exception as e:
            return rx.window_alert(f"Error creating proposal: {str(e)}")