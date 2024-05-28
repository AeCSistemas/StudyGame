from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Substitua por uma chave secreta forte
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@host:port/database'  # Configure a URI do PostgreSQL
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Aluno(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    serie = db.Column(db.String(50), nullable=False)
    nome_pai = db.Column(db.String(100), nullable=False)
    nome_mae = db.Column(db.String(100), nullable=False)
    escola_cnpj = db.Column(db.String(18), nullable=False)

    def __repr__(self):
        return '<Aluno %r>' % self.nome

@app.route('/')
def index():
    if 'user_id' in session:
        return render_template('index.html')
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('signup'))
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash('Logged in successfully!')
            return redirect(url_for('index'))
        else:
            flash('Incorrect username or password')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('Logged out successfully!')
    return redirect(url_for('index'))

@app.route('/cadastrar_aluno', methods=['GET', 'POST'])
def cadastrar_aluno():
    if request.method == 'POST':
        nome = request.form['nome']
        data_nascimento = request.form['data_nascimento']
        serie = request.form['serie']
        nome_pai = request.form['nome_pai']
        nome_mae = request.form['nome_mae']
        escola_cnpj = request.form['escola_cnpj']

        novo_aluno = Aluno(nome=nome, data_nascimento=data_nascimento, serie=serie,
                           nome_pai=nome_pai, nome_mae=nome_mae, escola_cnpj=escola_cnpj)
        db.session.add(novo_aluno)
        db.session.commit()
        flash('Aluno cadastrado com sucesso!')
        return redirect(url_for('index'))

    return render_template('cadastrar_aluno.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)