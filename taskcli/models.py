from dataclasses import dataclass,  field
from typing import List, Optional

@dataclass
class Task:
    id: int
    title: str
    created_at: str
    status: str = "aberto"
    priority: str = "médio"
    description: str = ""
    due: Optional[str] = None
    tags: List[str] = field(default_factory=list)

    def to_dict(self):
        """Conveerte a tarefa (Objeto) em um dicionário (JSON)."""
        return {
            "id": self.id,
            "title": self.title,
            "created_at": self.created_at,
            "status": self.status,
            "priority": self.priority,
            "description": self.description,
            "due": self.due,
            "tags": self.tags,
        }
    
    @classmethod
    def from_dict(cls, data):
        """Cria uma tarefa (Objeto) a partir de um dicionário (JSON)."""
        #garante que as tags sejam sempre uma lista, mesmo se vier vazio do JSON
        if "tags" not in data or data["tags"] is None:
            data["tags"] = []
        return cls(**data)