from dataclasses import dataclass

@dataclass
class ProcessingError:
    code: str
    message: str
