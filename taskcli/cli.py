import argparse
from typing import List, Optional
from taskcli import storage, utils
from taskcli.models import Task

# --- FUNÇÕES DE COMANDO (A Lógica) ---

def cmd_init(args):
    """Cria a estrutura de pastas."""
    print("Inicializando TaskCLI...")
    storage._ensure_db_exists()
    print(f"Pronto! Banco de dados em: {storage.DATA_FILE}")

def cmd_add(args):
    """Adiciona uma nova tarefa."""
    tasks = storage.load_tasks()
    
    # Valida a data se ela foi passada
    if args.due and not utils.validate_date(args.due):
        print(f"ERRO: Data '{args.due}' inválida. Use o formato YYYY-MM-DD.")
        return

    # Processa as tags (separa por vírgula e remove espaços)
    tags_list = [t.strip() for t in args.tags.split(',')] if args.tags else []

    new_task = Task(
        id=storage.get_next_id(tasks),
        title=args.title,
        description=args.desc,
        created_at=utils.get_today_iso(),
        due=args.due,
        priority=args.priority,
        tags=tags_list,
        status="aberto"
    )

    tasks.append(new_task)
    storage.save_tasks(tasks)
    print(f"✅ Tarefa {new_task.id} criada: '{new_task.title}'")

def cmd_list(args):
    """Lista as tarefas com filtros."""
    tasks = storage.load_tasks()
    
    if not tasks:
        print("Nenhuma tarefa encontrada.")
        return

    # Filtragem
    filtered = tasks
    if not args.all:
        filtered = [t for t in filtered if t.status == "aberto"]
    
    if args.priority:
        filtered = [t for t in filtered if t.priority == args.priority]
    
    if args.tag:
        filtered = [t for t in filtered if args.tag in t.tags]

    # Exibição (Tabela simples)
    print(f"{'ID':<4} | {'Status':<8} | {'Prioridade':<10} | {'Due':<10} | {'Título'}")
    print("-" * 60)
    
    for t in filtered:
        due_str = t.due if t.due else ""
        print(f"{t.id:<4} | {t.status:<8} | {t.priority:<10} | {due_str:<10} | {t.title}")

def cmd_done(args):
    """Marca tarefa como feita."""
    tasks = storage.load_tasks()
    
    found = False
    for t in tasks:
        if t.id == args.id:
            t.status = "feito"
            found = True
            break
            
    if found:
        storage.save_tasks(tasks)
        print(f"✅ Tarefa {args.id} marcada como feita.")
    else:
        print(f"❌ Tarefa {args.id} não encontrada.")

def cmd_remove(args):
    """Remove uma tarefa."""
    tasks = storage.load_tasks()
    
    # Filtra mantendo apenas as tarefas que NÃO são a que queremos remover
    original_count = len(tasks)
    tasks = [t for t in tasks if t.id != args.id]
    
    if len(tasks) < original_count:
        storage.save_tasks(tasks)
        print(f"🗑️ Tarefa {args.id} removida.")
    else:
        print(f"❌ Tarefa {args.id} não encontrada.")

def cmd_update(args):
    """Atualiza campos de uma tarefa."""
    tasks = storage.load_tasks()
    
    task = next((t for t in tasks if t.id == args.id), None)
    if not task:
        print(f"❌ Tarefa {args.id} não encontrada.")
        return

    if args.title: task.title = args.title
    if args.priority: task.priority = args.priority
    if args.due: 
        if utils.validate_date(args.due):
            task.due = args.due
        else:
            print("Data inválida ignorada.")
    
    storage.save_tasks(tasks)
    print(f"✅ Tarefa {args.id} atualizada.")

# --- CONFIGURAÇÃO DO ARGPARSE (O Tradutor) ---

def main():
    parser = argparse.ArgumentParser(description="TaskCLI - Gerenciador de Tarefas")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Comando: init
    parser_init = subparsers.add_parser('init', help='Inicializa o banco de dados')
    parser_init.set_defaults(func=cmd_init)

    # Comando: add
    parser_add = subparsers.add_parser('add', help='Adiciona tarefa')
    parser_add.add_argument('title', help='Título da tarefa')
    parser_add.add_argument('--desc', default="", help='Descrição')
    parser_add.add_argument('--priority', choices=['alto', 'médio', 'baixo'], default='médio')
    parser_add.add_argument('--due', help='Data de vencimento (YYYY-MM-DD)')
    parser_add.add_argument('--tags', help='Tags separadas por vírgula')
    parser_add.set_defaults(func=cmd_add)

    # Comando: list
    parser_list = subparsers.add_parser('list', help='Lista tarefas')
    parser_list.add_argument('--all', action='store_true', help='Mostra também as feitas')
    parser_list.add_argument('--priority', help='Filtra por prioridade')
    parser_list.add_argument('--tag', help='Filtra por tag')
    parser_list.set_defaults(func=cmd_list)

    # Comando: done
    parser_done = subparsers.add_parser('done', help='Marca como feita')
    parser_done.add_argument('id', type=int, help='ID da tarefa')
    parser_done.set_defaults(func=cmd_done)

    # Comando: remove
    parser_remove = subparsers.add_parser('remove', help='Remove tarefa')
    parser_remove.add_argument('id', type=int, help='ID da tarefa')
    parser_remove.set_defaults(func=cmd_remove)

    # Comando: update
    parser_update = subparsers.add_parser('update', help='Atualiza tarefa')
    parser_update.add_argument('id', type=int, help='ID da tarefa')
    parser_update.add_argument('--title', help='Novo título')
    parser_update.add_argument('--priority', choices=['alto', 'médio', 'baixo'])
    parser_update.add_argument('--due', help='Nova data')
    parser_update.set_defaults(func=cmd_update)

    # Processa os argumentos
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()