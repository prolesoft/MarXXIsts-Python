from os import path, remove, mkdir
from flask import (
    Flask,
    escape,
    request,
    render_template,
    redirect,
    flash,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import current_user, login_user, LoginManager, logout_user, login_required
import pypandoc

app = Flask(__name__)

if path.isfile("config.cfg"):
    app.config.from_pyfile("config.cfg")

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"


# circular dependencies, these imports need to be down here
from forms import *
from models import *


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = UserAccount(
            form.display_name.data,
            form.username.data,
            form.email.data,
            form.password.data,
        )
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = UserAccount.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/upload", methods=['GET', 'POST'])
@login_required
def upload():
    form = DocumentUploadForm()
    if form.validate_on_submit():
        print("hi")
        f = form.document.data
        filename = secure_filename(f.filename)
        print(filename)
        works_directory = 'works'
        converted_directory = path.join(works_directory, 'converted')
        filepath = path.join(works_directory, filename)
        if not path.exists(converted_directory):
            if not path.exists(works_directory):
                mkdir(works_directory)
            mkdir(converted_directory)
        
        f.save(filepath)
        converted_filepath = path.join('works', 'converted', f"{filename}.html")
        pypandoc.convert_file(filepath, 'html', outputfile=converted_filepath)
        remove(filepath)
        doc = Document(current_user.id, form.title.data, converted_filepath)
        db.session.add(doc)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('upload.html', form=form)