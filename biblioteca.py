# Sistema de Biblioteca Escolar
from datetime import date

livros = []  # lista de dicionários
MULTA_POR_DIA = 2.0


# ── FUNÇÕES AUXILIARES ──────────────────────────────────

def buscar(codigo):
    for livro in livros:
        if livro["codigo"] == codigo.upper():
            return livro
    return None

def formatar(data):
    return data.strftime("%d/%m/%Y") if data else "—"

def ler_data(msg):
    while True:
        try:
            return date.fromisoformat(input(msg))  # formato AAAA-MM-DD
        except ValueError:
            print("  Data inválida! Use AAAA-MM-DD.")


# ── FUNÇÕES PRINCIPAIS ──────────────────────────────────

def cadastrar_livro():
    titulo = input("Título: ")
    autor  = input("Autor: ")
    codigo = input("Código (ex: LIV-001): ").upper()

    if not titulo or not autor or not codigo:
        print("❌ Preencha todos os campos!")
        return
    if buscar(codigo):
        print("❌ Código já cadastrado!")
        return

    livros.append({
        "codigo": codigo,
        "titulo": titulo,
        "autor": autor,
        "disponivel": True,
        "aluno": None,
        "data_devolucao": None,
    })
    print(f"✅ '{titulo}' cadastrado!")


def registrar_emprestimo():
    codigo = input("Código do livro: ").upper()
    livro  = buscar(codigo)

    if not livro:
        print("❌ Livro não encontrado!")
        return
    if not livro["disponivel"]:
        print(f"❌ Emprestado para {livro['aluno']}.")
        return

    livro["aluno"]         = input("Nome do aluno: ")
    livro["data_devolucao"] = ler_data("Prazo de devolução (AAAA-MM-DD): ")
    livro["disponivel"]    = False
    print(f"✅ Emprestado para {livro['aluno']} até {formatar(livro['data_devolucao'])}.")


def registrar_devolucao():
    codigo = input("Código do livro: ").upper()
    livro  = buscar(codigo)

    if not livro:
        print("❌ Livro não encontrado!")
        return
    if livro["disponivel"]:
        print("⚠️ Livro já está disponível.")
        return

    data_real = ler_data("Data de devolução (AAAA-MM-DD): ")
    atraso    = (data_real - livro["data_devolucao"]).days

    print(f"✅ Devolvido por {livro['aluno']}.", end=" ")
    if atraso > 0:
        print(f"⚠️ Multa: R$ {atraso * MULTA_POR_DIA:.2f} ({atraso} dia(s) de atraso).")
    else:
        print("Sem multa.")

    livro["disponivel"]    = True
    livro["aluno"]         = None
    livro["data_devolucao"] = None


def listar_livros():
    if not livros:
        print("Nenhum livro cadastrado.")
        return

    print(f"\n{'─'*55}")
    print(f"{'Código':<10} {'Título':<25} {'Status':<15} {'Aluno'}")
    print(f"{'─'*55}")
    for l in livros:
        if l["disponivel"]:
            status = "✅ Disponível"
            aluno  = "—"
        elif l["data_devolucao"] < date.today():
            status = "⚠️ Atrasado"
            aluno  = l["aluno"]
        else:
            status = "📤 Emprestado"
            aluno  = l["aluno"]
        print(f"{l['codigo']:<10} {l['titulo']:<25} {status:<15} {aluno}")
    print()


# ── MENU ───────────────────────────────────────────────

def menu():
    # Dados de exemplo
    livros.extend([
        {"codigo": "LIV-001", "titulo": "O Pequeno Príncipe", "autor": "Saint-Exupéry",
         "disponivel": True, "aluno": None, "data_devolucao": None},
        {"codigo": "LIV-002", "titulo": "Dom Casmurro", "autor": "Machado de Assis",
         "disponivel": False, "aluno": "Pedro Alves", "data_devolucao": date(2026, 4, 17)},
    ])

    opcoes = {
        "1": ("Cadastrar livro",       cadastrar_livro),
        "2": ("Registrar empréstimo",  registrar_emprestimo),
        "3": ("Registrar devolução",   registrar_devolucao),
        "4": ("Listar livros",         listar_livros),
    }

    while True:
        print("\n📚 BIBLIOTECA ESCOLAR")
        for k, (nome, _) in opcoes.items():
            print(f"  {k}. {nome}")
        print("  0. Sair")

        op = input("Opção: ")
        if op == "0":
            print("Até logo! 👋")
            break
        elif op in opcoes:
            opcoes[op][1]()
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()
