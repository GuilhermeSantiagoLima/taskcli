from taskcli.models import Task

def test_criar_tarefa_simples():
    """Testa se conseguimos criar uma tarefa básica."""
    t = Task(id=1, title="Teste", created_at="2025-01-01")
    
    assert t.title == "Teste"
    assert t.status == "aberto"  # Verifica o valor padrão
    assert t.priority == "médio" # Verifica o valor padrão
    assert t.tags == []          # Verifica se a lista veio vazia

def test_converter_para_dict():
    """Testa se o método to_dict funciona para salvar no JSON."""
    t = Task(id=1, title="Teste", created_at="2025-01-01")
    dados = t.to_dict()
    
    assert dados['id'] == 1
    assert dados['title'] == "Teste"
    assert dados['status'] == "aberto"

def test_tags_sao_independentes():
    """
    Testa aquele erro clássico da lista compartilhada.
    Se eu mudar a tag da Tarefa 1, a Tarefa 2 NÃO pode mudar.
    """
    t1 = Task(id=1, title="T1", created_at="Hoje")
    t2 = Task(id=2, title="T2", created_at="Hoje")
    
    t1.tags.append("urgente")
    
    assert "urgente" in t1.tags
    assert "urgente" not in t2.tags  # Isso garante que o field(default_factory) funcionou!