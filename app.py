from flask import Flask, escape, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm

app = Flask(__name__)
app.config.from_pyfile('config.cfg')
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from forms import RegistrationForm
from models import *

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = UserAccount(form.display_name.data, form.username.data, form.email.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    return render_template('register.html', form=form)
    