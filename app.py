from flask import Flask, render_template, request, redirect
from datetime import date

app = Flask(__name__)

# ── DADOS ──────────────────────────────────────────────
livros = [
    {"codigo": "LIV-001", "titulo": "O Pequeno Príncipe", "autor": "Saint-Exupéry",
     "disponivel": True, "aluno": None, "data_devolucao": None},
    {"codigo": "LIV-002", "titulo": "Dom Casmurro", "autor": "Machado de Assis",
     "disponivel": False, "aluno": "Pedro Alves", "data_devolucao": date(2026, 4, 17)},
]

MULTA_POR_DIA = 2.0
mensagem = {"texto": "", "tipo": ""}


def buscar(codigo):
    for l in livros:
        if l["codigo"] == codigo.upper():
            return l
    return None

def set_msg(texto, tipo="sucesso"):
    mensagem["texto"] = texto
    mensagem["tipo"]  = tipo


# ── ROTAS ───────────────────────────────────────────────

@app.route("/")
def index():
    msg = mensagem.copy()
    mensagem["texto"] = ""  # limpa após exibir
    return render_template("index.html", livros=livros, msg=msg, hoje=date.today())


@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    titulo = request.form["titulo"].strip()
    autor  = request.form["autor"].strip()
    codigo = request.form["codigo"].strip().upper()

    if not titulo or not autor or not codigo:
        set_msg("Preencha todos os campos!", "erro")
    elif buscar(codigo):
        set_msg(f"Código '{codigo}' já cadastrado!", "erro")
    else:
        livros.append({"codigo": codigo, "titulo": titulo, "autor": autor,
                       "disponivel": True, "aluno": None, "data_devolucao": None})
        set_msg(f"'{titulo}' cadastrado com sucesso!")

    return redirect("/")


@app.route("/emprestar", methods=["POST"])
def emprestar():
    codigo = request.form["codigo"].strip().upper()
    aluno  = request.form["aluno"].strip()
    data   = request.form["data_devolucao"]
    livro  = buscar(codigo)

    if not livro:
        set_msg("Livro não encontrado!", "erro")
    elif not livro["disponivel"]:
        set_msg(f"Livro já emprestado para {livro['aluno']}!", "erro")
    elif not aluno or not data:
        set_msg("Preencha todos os campos!", "erro")
    else:
        livro["disponivel"]    = False
        livro["aluno"]         = aluno
        livro["data_devolucao"] = date.fromisoformat(data)
        set_msg(f"Emprestado para {aluno}!")

    return redirect("/")


@app.route("/devolver", methods=["POST"])
def devolver():
    codigo    = request.form["codigo"].strip().upper()
    data_real = request.form["data_real"]
    livro     = buscar(codigo)

    if not livro:
        set_msg("Livro não encontrado!", "erro")
    elif livro["disponivel"]:
        set_msg("Livro já está disponível!", "erro")
    else:
        atraso = (date.fromisoformat(data_real) - livro["data_devolucao"]).days
        texto  = f"'{livro['titulo']}' devolvido por {livro['aluno']}."
        if atraso > 0:
            texto += f" Multa: R$ {atraso * MULTA_POR_DIA:.2f}"
            set_msg(texto, "alerta")
        else:
            set_msg(texto)

        livro["disponivel"]    = True
        livro["aluno"]         = None
        livro["data_devolucao"] = None

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
