from dataclasses import dataclass, field

@dataclass
class ValidationContext:
    seen_claim_ids: set[str] = field(default_factory=set) # Create new empty set per object creation