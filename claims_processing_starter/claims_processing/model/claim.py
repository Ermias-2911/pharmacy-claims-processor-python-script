from dataclasses import dataclass

@dataclass
class Claim:
    claim_id: str
    member_id: str
    ndc: str
    date_of_service: str
    quantity: int | str
    days_supply: int | str
    drug_cost: float | str
    plan_type: str
