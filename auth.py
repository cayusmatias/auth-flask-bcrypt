import bcrypt
import functools
from flask import Blueprint, redirect, request, session, url_for, flash
import sqlite3


def conectabd():
    return sqlite3.connect('sqlite3.db')


def commit_db(sql):
    conn = sqlite3.connect('sqlite3.db')
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


auth = Blueprint("auth", __name__)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if not 'user' in session.keys():
            flash('warning')
            flash('Você precisa estar logado para acessar esse recurso.')
            return redirect("/")
        return view(**kwargs)
    return wrapped_view


@auth.route('/login', methods=['POST'])
def login():
    session.permanent = True

    username = request.form['username']
    password = request.form['password'].encode('utf-8')
    hashedpass = bcrypt.hashpw(password, bcrypt.gensalt(10))
    print(hashedpass)

    cursor = conectabd().cursor()
    cursor.execute(f"SELECT * FROM users WHERE user = '{username}'")
    userexist = cursor.fetchone()
    if userexist is not None:
        if bcrypt.checkpw(password, userexist[2].encode('utf-8')):
            session['user'] = username
            return redirect('/dashboard')
        else:
            flash('danger')
            flash('Usuário ou Senha incorretos')
            return redirect('/')
    else:
        flash('danger')
        flash('Usuário ou Senha incorretos')
        return redirect('/')


@auth.route('/register_user', methods=['POST'])
def register_user():
    username = request.form['usuario']
    password = request.form['password'].encode('utf-8')
    passconfirmation = request.form['passconfirmation'].encode('utf-8')

    cursor = conectabd().cursor()
    cursor.execute(f"SELECT COUNT(*) FROM users WHERE user = '{username}'")
    userexist = cursor.fetchone()[0]

    if password != passconfirmation:
        flash('danger')
        flash('Senhas não são iguais')
        return redirect('/register')

    if userexist > 0:
        flash('danger')
        flash('Usuário já cadastrado')
        return redirect('/register')

    hashedpass = bcrypt.hashpw(password, bcrypt.gensalt(10))

    commit_db(f"INSERT INTO users (user, password) VALUES ('{username}', '{hashedpass.decode('utf-8')}')")
    flash('success')
    flash(f'Usuário {username} cadastrado com sucesso')
    return redirect('/register')


@auth.route('/logout')
def logout():
    session.clear()
    flash('success')
    flash('Logout realizado com sucesso')
    return redirect('/')

