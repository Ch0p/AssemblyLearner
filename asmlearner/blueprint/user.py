from flask import Blueprint, render_template, abort, g, session, redirect
from jinja2 import TemplateNotFound
from asmlearner.middleware import *
from hashlib import sha1

user = Blueprint('user', __name__)


@user.route('/login')
def login():
    return render_template('login.html', title='AL User Login', action='/login', submit='Login', next_link='/join',
            next='Create User')


@user.route('/login', methods=['POST'])
def login_check():
    id_ = request.form['id']
    password_ = request.form['password']
    pw_hash = sha1(password_.encode('utf8') * 10).hexdigest()

    user = g.db.query('SELECT * FROM user WHERE id=? AND password=?', (id_, pw_hash), True)

    if user is None:
        return '''
            <script>
                alert("ID or PW is incorrect");
                history.back(-1);
            </script>       
        '''
    else:
        user = dict(user)
        session['user'] = user
        return redirect('/problems')


@user.route('/logout')
@login_required
def logout():
    del session['user']
    return redirect('/')


@user.route('/join')
def join():
    return render_template('login.html', title="AL User Create", action="/join", submit='Join', next_link='/login',
            next='Login As User')


@user.route('/join', methods=['POST'])
def join_check():
    id_ = request.form['id']
    password_ = request.form['password']
    pw_hash = sha1(password_.encode('utf8') * 10).hexdigest()

    user = g.db.query('SELECT 1 FROM user WHERE id=?', (id_,), True)

    if user is None:
        try:
            g.db.execute('INSERT INTO user (id, password) VALUES(?, ?)', (id_, pw_hash))
            g.db.commit()
        except:
            g.db.rollback()
        return '''
            <script>
                alert('Successfully created user!');
                location.href='/login';
            </script>
        '''
    else:
        return '''
            <script>
                alert('User already exists!');
                history.back(-1);
            </script>
        '''
