from flask import Flask, render_template, redirect, request, jsonify, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.messages import Messages
from forms import RegisterForm, LoginForm, MessageForm
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'test_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


def main():
    db_session.global_init("db/base.sqlite")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.args:
        message = request.args['messages']
    else:
        message = ""
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Sign in', form=form, message=message)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/chat", methods=['GET', 'POST'])
def chat():
    if not current_user.is_authenticated:
        messages = "Чат доступен только авторизованным пользователям"
        return redirect(url_for('.login', messages=messages))
    form = MessageForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        messages = Messages()
        messages.content = form.content.data
        current_user.messages.append(messages)
        session.merge(current_user)
        session.commit()
        return redirect('/chat')
    session = db_session.create_session()
    messages = session.query(Messages)
    return render_template("chat.html", messages=messages, form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            email=form.email.data,
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route("/", methods=['GET'])
def home():
    return render_template('home.html', title='Главная')


# API
@app.route('/api/register', methods=['POST'])
def register_api():
    req = request.get_json()
    if not req:
        return jsonify({'error': 'Empty request'})
    email = req["email"]
    password = req["password"]
    if email is None or password is None:
        return jsonify({'error': 'Empty request'})
    session = db_session.create_session()
    if session.query(User).filter(User.email == email).first():
        return jsonify({'error': 'User exists'})
    user = User(email=email)
    user.set_password(password)
    session.add(user)
    session.commit()
    return jsonify({'success': 'OK'})


@app.route('/api/login', methods=['POST'])
def login_api():
    req = request.get_json()
    if not req:
        return jsonify({'error': 'Empty request'})
    email = req["email"]
    password = req["password"]
    if email is None or password is None:
        return jsonify({'error': 'Empty request'})
    session = db_session.create_session()
    user = session.query(User).filter(User.email == email).first()
    if user and user.check_password(password):
        login_user(user)
        return jsonify({'success': 'OK'})
    return jsonify({'error': 'Incorrect login or password'})


@app.route('/api/logout')
def logout_api():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'})
    logout_user()
    return jsonify({'success': 'OK'})


@app.route('/api/data')
def data_api():
    if not current_user.is_authenticated:
        return jsonify({'error': 'Unauthorized'})
    result = {"id": current_user.id, "email": current_user.email}
    return jsonify(result)


if __name__ == '__main__':
    main()
