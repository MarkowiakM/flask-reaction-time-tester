from flask import Flask, redirect, request, render_template, g, session, url_for
import database as db_fun
from werkzeug.security import generate_password_hash, check_password_hash
from validate import ValidEmail, ValidPassword
import os
from datetime import date


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def get_user_from_session():
    user = None
    if 'user' in session:
        email = session['user']
        db = db_fun.get_db()
        user = db.execute('select id, email, passwd from users where email = ?', [
                          email]).fetchone()
    return user


def check_valid_email(email):
    return (ValidEmail(email)).email


def check_valid_password(password):
    return (ValidPassword(password)).password


def add_user_to_session(input_email, input_password):
    db = db_fun.get_db()
    user = db_fun.get_user(db, input_email).fetchone()
    if user and check_password_hash(user['passwd'], input_password):
        session['user'] = user['email']


@app.route('/', methods=['GET'])
def index():
    user = get_user_from_session()
    return render_template('home.html', user=user)


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        db = db_fun.get_db()
        given_email = request.form['email']
        given_password = request.form['password']
        given_conf_password = request.form['password-confirm']
        user = db_fun.get_user(db, given_email).fetchone()
        if user:
            return render_template('sign-up.html', duplicate_user=True)
        else:
            if check_valid_email(given_email) and check_valid_password(given_password) and given_conf_password == given_password:
                hashed_passwd = generate_password_hash(
                    given_password, method='sha256')
                db.execute('insert into users (email, passwd) values (?, ?)', [
                    given_email, hashed_passwd])
                db.commit()
                return render_template('login.html', signed_up=True)
            elif not check_valid_email(given_email):
                return render_template('sign-up.html', invalid_email=True)
            elif not check_valid_password(given_password):
                return render_template('sign-up.html', invalid_password=True)
            else:
                return render_template('sign-up.html', different_passwords=True)

    return render_template('sign-up.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        add_user_to_session(request.form['email'],  request.form['password'])
        if 'user' in session:
            return redirect(url_for('my_profile'))
        else:
            return render_template('login.html', wrong_data=True)
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))


@app.route('/my-profile')
def my_profile():
    user = get_user_from_session()
    db = db_fun.get_db()
    user_test_amount = db_fun.user_test_amount(db, user['id'])
    all_test_amount = db_fun.all_test_amount(db)
    user_best_result = db_fun.user_best_result(db, user['id']) or 0
    best_result = db_fun.best_result(db) or 0

    labels, values = None, None
    if db_fun.user_results_daily(db, user['id']):
        labels, values = db_fun.user_results_daily(db, user['id'])

    return render_template('my-profile.html', user=user, user_test_amount=user_test_amount, all_test_amount=all_test_amount, user_best_result=user_best_result, best_result=best_result, labels=labels, values=values)


@app.route('/time-tester', methods=['GET', 'POST'])
def time_tester():
    user = get_user_from_session()
    if request.method == 'POST':
        db = db_fun.get_db()
        result = request.form['input']
        db.execute('insert into results (userId, result, resultDate) values (?, ?, ?)', [
            user['id'], result, date.today()])
        db.commit()
        return redirect(url_for('my_profile'))

    return render_template('time-tester.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
