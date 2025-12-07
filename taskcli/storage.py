import json
import os
from pathlib import Path
from typing import List
from taskcli.models import Task  # Veja! Ele usa o models que já criamos.

# Define onde o arquivo vai ser salvo (pasta do usuário/.taskcli)
DATA_DIR = Path.home() / ".taskcli"
DATA_FILE = DATA_DIR / "tasks.json"

def _ensure_db_exists():
    """Garante que a pasta e o arquivo JSON existem."""
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    if not DATA_FILE.exists():
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

def load_tasks() -> List[Task]:
    """Lê o arquivo JSON e retorna uma lista de Tarefas."""
    _ensure_db_exists()
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return [Task.from_dict(item) for item in data]
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_tasks(tasks: List[Task]):
    """Recebe a lista de Tarefas e salva no arquivo JSON."""
    _ensure_db_exists()
    
    data = [task.to_dict() for task in tasks]
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def get_next_id(tasks: List[Task]) -> int:
    """Calcula o próximo ID disponível."""
    if not tasks:
        return 1
    return max(task.id for task in tasks) + 1