from flask import Flask, render_template, request, jsonify
import mysql.connector
import random
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'teste@123'

banco = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123@",
    database="db_alunossala"
)

cursor = banco.cursor()

personagem = "https://rickandmortyapi.com/api/character/"

@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    nome = request.form.get('nome')
    senha = request.form.get('senha')

    if nome == 'usuario.teste' and senha == 'teste@123':
        return render_template("home.html"), 200
    else:
        return render_template("login.html"), 407


@app.route('/alunos', methods=['GET'])
def get_alunos():
    cursor.execute("SELECT * FROM alunos")
    alunos = cursor.fetchall()
    return jsonify(alunos)


@app.route('/cadastro/<nome>/<idade>/<id_char>', methods=['GET','POST'])
def add_aluno(nome,idade,id_char):

    sql = "INSERT INTO personagem (Nome, Idade, Num_Personagem) VALUES (%s, %s, %s)"
    val = (nome, int(idade), int(id_char))
    cursor.execute(sql, val)
    banco.commit()

    return "Aluno cadastrado com sucesso"


@app.route('/apagar/<nome>', methods=['GET','DELETE'])
def del_aluno(nome):

    sql = "DELETE FROM personagem WHERE Nome = %s"
    val = (nome,)

    cursor.execute(sql, val)
    banco.commit()

    return "Aluno excluído com sucesso"

# Mostra o Aluno e seu Personagem favorito
@app.route('/char/<nome>', methods=['GET'])
def char_aluno(nome):
    sql = "SELECT Nome,Num_personagem from personagem WHERE Nome = %s"
    val = (nome,)

    cursor.execute(sql, val) 
    resultado = cursor.fetchall()
    nome_aluno = str(resultado[0][0])
    per_aluno = str(resultado[0][1])

    personagem_aluno = requests.get(personagem + per_aluno)
    b = personagem_aluno.json()

    per_aluno = b['name']
    return f'O personagem favorito de {nome_aluno} é {per_aluno}.'

@app.route('/gerar_personagem', methods=['GET'])
def gerar_char():
    Id = random.randint(1,826)
    char_aleatorio = requests.get(personagem + str(Id))
    b = char_aleatorio.json()
    return f"Seu char aleatorio é: {b['name']} e seu ID é: {b['id']}."




if __name__ == "__main__":
    app.run(debug=True)
