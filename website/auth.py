import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import (login_user, login_required,
                         logout_user, current_user)
from random import shuffle
from .models import User


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
            flash('Voce já está logado.', category='error')
            return redirect(url_for('views.home'))
    elif request.method == 'POST':        
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash(f'Seja bem-vindo(a) {user.first_name}', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta, tente novamente.', category='error')
        else:
            flash('Email não cadastrado.', category='error')
    return render_template('login.html', user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if current_user.is_authenticated:
            flash('Voce já está logado.', category='error')
            return redirect(url_for('views.home'))
    elif request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email já existe.', category='error')
        elif len(email) < 4:
            flash('Email deve ter mais que 3 caracteres', category='error')
        elif len(first_name) < 4:
            flash('Primeiro nome deve ter mais que 3 letras',
                  category='error')
        elif password1 != password2:
            flash('Senhas diferentes', category='error')
        elif len(password1) < 7:
            flash('A senha deve possuir pelo menos 7 caracteres.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            songs_path = f'./website/static/users/{str(new_user.id)}'
            os.makedirs(songs_path)

            path = os.path.join(songs_path, 'songs')
            os.makedirs(path)

            login_user(new_user, remember=True)

            flash('Conta criada!', category='success')
            return redirect(url_for('views.home'))

    return render_template('sign_up.html', user=current_user)
