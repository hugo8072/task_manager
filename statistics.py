from loads import load_tasks, load_users
from collections import Counter

def total_tasks_per_user():
    """
    Print total number of tasks per user.
    """
    users = load_users()
    print("\n--- Total Number of Tasks Per User ---")
    for username in users:
        tasks = load_tasks(username)
        print(f"{username}: {len(tasks)} task(s)")

def percentage_completed_per_user():
    """
    Print percentage of completed tasks per user.
    """
    users = load_users()
    print("\n--- Percentage of Completed Tasks Per User ---")
    for username in users:
        tasks = load_tasks(username)
        total = len(tasks)
        completed = sum(1 for t in tasks if t.get("completed", False))
        percent = (completed / total * 100) if total else 0
        print(f"{username}: {percent:.2f}% completed ({completed}/{total})")

def unique_tasks_per_category():
    """
    Print unique tasks per category (using a set).
    """
    users = load_users()
    category_tasks = {}
    for username in users:
        tasks = load_tasks(username)
        for t in tasks:
            cat = t.get("category", "Uncategorized")
            if cat not in category_tasks:
                category_tasks[cat] = set()
            category_tasks[cat].add(t.get("title", "Untitled"))
    print("\n--- Unique Tasks Per Category ---")
    for cat, titles in category_tasks.items():
        print(f"{cat}: {len(titles)} unique task(s)")

def most_used_categories():
    """
    Print the most used categories.
    """
    users = load_users()
    all_categories = [
        t.get("category", "Uncategorized")
        for username in users
        for t in load_tasks(username)
    ]
    counter = Counter(all_categories)
    if not counter:
        print("\nNo categories found.")
        return
    max_count = max(counter.values())
    most_used = [cat for cat, count in counter.items() if count == max_count]
    print("\n--- Most Used Categories ---")
    print(f"{', '.join(most_used)} ({max_count} task(s))") # type: ignore

def statistics_menu():
    while True:
        print("\n--- Menu de Estatísticas ---")
        print("1. Total de tarefas por utilizador")
        print("2. Percentagem de tarefas concluídas por utilizador")
        print("3. Tarefas únicas por categoria")
        print("4. Categorias mais usadas")
        print("0. Voltar")
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            total_tasks_per_user()
        elif opcao == "2":
            percentage_completed_per_user()
        elif opcao == "3":
            unique_tasks_per_category()
        elif opcao == "4":
            most_used_categories()
        elif opcao == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")

# Para testar diretamente:
if __name__ == "__main__":
    statistics_menu()