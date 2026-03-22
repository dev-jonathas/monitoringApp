from dataclasses import dataclass

@dataclass
class Alerta:
    error_id: str
    description: str
    action: str
    overview: str