import os
from flask import Flask, url_for, render_template, request, redirect, session, escape, flash, render_template_string

from personal_inventory.data import data as dal
from personal_inventory.defaultconfigs import ProductionDataConfig, TestingDataConfig
from personal_inventory.logic.user_logic import UserLogic

app = Flask(__name__)

env = os.environ.get('ENV')
if env == 'PROD':
    dal.configure(ProductionDataConfig)
    app.config.from_object('config.ProductionFlaskConfig')
elif env == 'TESTING':
    if os.environ.get('DATA') == 'PROD':
        dal.configure(ProductionDataConfig)
    else:
        dal.configure(TestingDataConfig)
    app.config.from_object('config.TestingFlaskConfig')
else:
    if os.environ.get('DATA') == 'PROD':
        dal.configure(ProductionDataConfig)
    else:
        dal.configure(TestingDataConfig)
    app.config.from_object('config.DevelopmentFlaskConfig')


@app.route('/')
def home():
    # if 'user_id' in session:
    # return render_template('home.html')
    #   user_id = session['user_id']
    #   ul = UserLogic()
    #  user = ul.get_by_id(user_id)
    # return 'Welcome {0} {1}'.format(user.firstname, user.lastname)
    # else:
    # return redirect(url_for('login'))
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_email = request.form['username_email']
        password = request.form['password']
        ul = UserLogic()
        if ul.validate_login(username_email, password):
            session['user_id'] = ul.get_by_username_email(username_email).id
            # flash('You were successfully logged in')
            return redirect(url_for('home'))
        else:
            # flash ... error ...
            pass
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))


@app.route('/register')
def register():
    return render_template_string(
        '''{% extends "layout.html" %}
{% block main %}
<div class="text-center">
  <h1>User registration</h1>
  <p class="lead">
    User registration not implemented.<br>
    Go <a href="javascript:void(0)" onclick="window.history.back()">back</a>.
  </p>
</div>
{% endblock %}''')


@app.route('/items')
def items():
    if 'user_id' in session:
        ul = UserLogic()
        user = ul.get_by_id(session['user_id'])
        items = user.items
        return render_template('items.html', items=items)
    return redirect(url_for('home'))
