import reflex as rx

class Proposal(rx.Model, table=True):
    title: str
    description: str
    end_time: int
    for_votes: int
    against_votes: int
    executed: bool
    proposer: str