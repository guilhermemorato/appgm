# este arquivo em Python conterá elementos do framework FLASK

#import os elementos do framework Flask para serem usados
from flask import Flask, render_template, request

# importa também do Flask o método REDIRECT
from flask import redirect

# importa o método de acesso Python a SQL
from cs50 import SQL

# informa ao Flask para considerar este arquivo de código Python (app.py) COMO uma aplicação web
# Cria uma variável "app"
app = Flask(__name__)


# Cria variável "db" e vincula ela ao banco SQL "froshims.db
db = SQL("sqlite:///froshims.db")

# Cria uma lista Python com as MODALIDADES DISPONÍVEIS de esportes
MODALIDADES = ["Basquete", "Natação", "Futebol", "Judo", "Ginástica Artistica"]

# Função para rotear (para /)
@app.route("/")
    # define uma função
def indice():
    # Chama a função FLASK "render_template" que busca o conteúdo de index.html (dentro do
    # diretório /template) e RENDERIZA o template index.html numa página
    # E desta vez, envia um parâmetro "modalidades" e informa que o conteúdo dele é a lista
    return render_template("index.html", modalidades = MODALIDADES)


# Função para rotear (para /matricula)
# inclui o método que precisamos (e não é o default "get") chamado POST
@app.route("/matricula", methods=["POST"])
def matricula():

    # testa se foram armazenados valores nas variáveis "nome_inserido" e SE "modalidade" é uma das MODALIDADES
    if not request.form.get("nome_inserido"):
        # se não tiver nome, RENDERIZA página "falha" com mensagem especifica
        return render_template("falha.html", message="Nome do aluno não preenchido!")

    if request.form.get("modalidade") not in MODALIDADES:
        # se não tiver nome, RENDERIZA página "falha" com mensagem especifica
        return render_template("falha.html", message="Modalidade não Definida!")

    # se tudo estiver ok:

    # REGISTRA NO BANCO DE DADOS o aluno e a modalidade (na tabela "registrants")
    nome = request.form.get("nome_inserido")
    modalidade = request.form.get("modalidade")
    # salva o conteúdo de "nome_inserido" no campo "name" do db e
    # "modalidade" no campo "sport" do db
    # [usando "VALUES(?, ?)" seguido das variáveis PARA PREVENIR INJECTION ATTACKS!!]
    db.execute("INSERT INTO registrants (name, sport) VALUES(?, ?)", nome, modalidade)

    # Exibe a página de Matriculados
    # COM COMANDO REDIRECT !!??????? (PORQUE?)
    return redirect("/matriculados")

    # RENDERIZA página "sucesso", passando o nome e modalidade para a página
@app.route("/matriculados")
def matriculados():
    # Cria lista Python (matriculados)
    # Popula a lista LENDO O CONTEÚDO DO DB de matriculados
    matriculados = db.execute("SELECT * FROM registrants")

    # Cria o HTML estático baseado no template "matriculados.html"
    # passando os dados da variável "matriculado" através do marcador "marcador_matriculados"
    return render_template("matriculados.html", marcador_matriculados=matriculados)
