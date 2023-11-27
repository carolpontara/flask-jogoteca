from flask import Flask, flash, redirect, render_template, request, session, url_for

class Game:
    def __init__(self, name, category, console):
        self.name=name
        self.category=category
        self.console=console

#lista global
game1= Game('Tetris', 'Puzzle', 'Atari')
game2= Game('God of War', 'Rack n Slash', 'PS2')
game3= Game('Mortal Kombat', 'Luta', 'PS2')
games_list = [game1, game2, game3]

class User():
    def __init__(self, nome, nickname, senha):
        self.nome = nome
        self.nickname = nickname
        self.senha = senha

usuario1 = User("Carol Pontara", "Pontara", "123@")
usuario2 = User("Luiz Pontara", "Luizz", "fiatunoo@")
usuario3 = User("Clara Pontara", "Clarinha", "13032023")

user_list = { usuario1.nickname: usuario1 , usuario2.nickname: usuario2 , usuario3.nickname : usuario3 }


app = Flask(__name__)

#Camada de criptp
app.secret_key = 'alura'

@app.route('/')
def index():
    return render_template('list.html', title='JOGOS', games=games_list)


@app.route('/novo')
def cadastrar():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('new-game.html', title="Cadastre um novo Jogo")


@app.route('/criar', methods=['POST',])
def create():
    name = request.form['nome']
    category = request.form['categoria']
    console = request.form['console']
    game = Game(name, category, console)
    games_list.append(game)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima= request.args.get('proxima')
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods=['POST', ])
def autenticar():
    if request.form['usuario'] in user_list:
        usuario = user_list[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
        flash(usuario.nickname + ' logou com sucesso!')
        proxima_pag = request.form['proxima']
        return redirect(proxima_pag)
    else:
        flash('Usuário não logado.')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('index'))

app.run()