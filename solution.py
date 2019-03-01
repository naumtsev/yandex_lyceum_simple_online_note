from flask import Flask, render_template, request, redirect, session
import json
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, PasswordField
from wtforms.validators import DataRequired
from database import users, news
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e70lIUUoXRKlXc5VUBmiJ9Hdi'

ADMINS = json.loads(open('static/admins.txt', 'r', encoding='utf-8').read())



def is_admin(s, p):
    if s in ADMINS and ADMINS[s] == p:
        return True
    return False

class LoginForm(FlaskForm):
    user_name = StringField('Login:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Войти')

class AddNewsForm(FlaskForm):
    title = StringField('Заголовок:', validators=[DataRequired()])
    content = TextAreaField('Содержание:', validators=[DataRequired()])
    submit = SubmitField('Добавить')

class RegisterForm(FlaskForm):
    user_name = StringField('Login:', validators=[DataRequired()])
    password = StringField('Password:', validators=[DataRequired()])
    submit = SubmitField('Отправить')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data
        exists = users.exists(user_name, password)
        if (exists[0]):
            session['username'] = user_name
            session['user_id'] = exists[1]
            return redirect("/")
        else:
            return render_template('login.html', form=form, status=3)
    return render_template('login.html', form=form, status=1)


@app.route('/logout')
def logout():
    session.pop('username',0)
    session.pop('user_id',0)
    return redirect('/login')


@app.route('/', methods=['POST', 'GET'])
def index():
    if 'username' not in session:
        return redirect('/login')
    user_news = news.get_all(user_name=session['username'])
    if session['username'] in ADMINS:
        return render_template('index.html', news=user_news, sz=len(user_news), ADMINS=ADMINS, username=session['username'])
    return render_template('index.html', news=user_news, sz=len(user_news),ADMINS=ADMINS, username=session['username'])


@app.route('/users', methods=['POST', 'GET'])
def check_users():
    if 'username' not in session:
        return redirect('/login')

    if session['username'] not in ADMINS:
        return redirect('/')
    buffer = users.get_all()
    ALL_USERS = []
    for i in buffer:
        id = i[0]
        username=i[1]
        password=i[2]
        cnt=users.count_by_username(username)
        ALL_USERS.append((id, username, password, cnt))
    return render_template('users.html', users=ALL_USERS, ADMINS=ADMINS, username=session['username'])

@app.route('/add', methods=['POST', 'GET'])
def add_news():
    if 'username' not in session:
        return redirect('/login')

    form = AddNewsForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        news.insert(session['username'], title, content)
        return redirect('/')

    return render_template('add.html', form=form, ADMINS=ADMINS, username=session['username'])


@app.route('/del/<id>', methods=['POST', 'GET'])
def del_news(id):
    if 'username' not in session:
        return redirect('/login')
    info = news.get(id)

    if info and info[1] == session['username']:
        news.delete(id)
    return redirect('/')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'username' in session:
        return redirect('/')

    form = RegisterForm()

    if form.validate_on_submit():
        user_name = form.user_name.data
        password = form.password.data
        flag = users.user_name_is_free(user_name)
        if(flag and user_name not in ADMINS):
            users.insert(user_name, password)
            session['username'] = user_name
            buffer = users.exists(user_name, password)
            session['user_id'] = buffer[1]
            return redirect("/")
        else:
            return render_template('register.html', form=form, status=3)
        return redirect('/')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')