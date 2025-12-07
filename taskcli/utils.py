from datetime import date, datetime

def get_today_iso() -> str:
    """
    Retorna a data de hoje formatada como texto no padrão ISO (YYYY-MM-DD).
    Exemplo: '2025-10-04'
    """
    return date.today().isoformat()

def validate_date(date_text: str) -> bool:
    """
    Tenta ler uma string como data no formato YYYY-MM-DD.
    Retorna True se for válida, False se estiver errada.
    """
    try:
        # Tenta converter o texto em objeto data.
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False