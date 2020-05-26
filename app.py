from os import path, remove, environ, mkdir
import codecs
from flask import (
    Flask,
    escape,
    request,
    render_template,
    redirect,
    flash,
    url_for,
    abort,
)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from werkzeug.urls import url_parse
from werkzeug.utils import secure_filename
from flask_login import (
    current_user,
    login_user,
    LoginManager,
    logout_user,
    login_required
)
import pypandoc

app = Flask(__name__)

if path.isfile("config.cfg"):
    app.config.from_pyfile("config.cfg")
else:
    secret_key = environ.get("SECRET_KEY")
    database_uri = environ.get("SQLALCHEMY_DATABASE_URI")
    app.config["SECRET_KEY"] = secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
login_manager.login_view = "login"


# circular dependencies, these imports need to be down here
from forms import *
from models import *

# Error Handlers

@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(401)
def unauthorized(e):
    return render_template("401.html"), 401

# Routes

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
        login_user(new_user)
        mkdir(path.join('works', new_user.username)) # Create a works directory for the new user
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
        uploaded_document_file = form.document.data
        uploaded_document_file_name = secure_filename(uploaded_document_file.filename)

        temp_save_path = path.join('works', 'temp', uploaded_document_file_name)
        uploaded_document_file.save(temp_save_path)

        user_directory = path.join('works', current_user.username)
        document_directory_name = secure_filename(form.title.data)
        document_directory_path = path.join(user_directory, document_directory_name)
        mkdir(document_directory_path) # Create directory to store all versions of converted document
        converted_filepath = path.join(
                                        user_directory,
                                        document_directory_name,
                                       f"00_{document_directory_name}.html") # Prefix indicates version

        pypandoc.convert_file(temp_save_path, 'html', outputfile=converted_filepath)
        remove(temp_save_path)

        doc = Document(current_user.id, form.title.data, document_directory_path)
        db.session.add(doc)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('upload.html', form=form)


@app.route("/reupload/<int:document_id>", methods=['GET', 'POST'])
@login_required
def reupload(document_id):
    form = DocumentReuploadForm()
    document = Document.query.get(document_id)
    if form.validate_on_submit():
        uploaded_document_file = form.document.data
        uploaded_document_file_name = secure_filename(uploaded_document_file.filename)

        temp_save_path = path.join('works', 'temp', uploaded_document_file_name)
        uploaded_document_file.save(temp_save_path)

        user_directory = path.join('works', current_user.username)
        document_directory_name = secure_filename(document.title)
        document_directory_path = path.join(user_directory, document_directory_name)

        version_number = int((sorted(listdir(document.path))[::-1][:1][0]).split("_")[0])
        version_string = f"0{version_number+1}" if version_number < 9 else f"{version_number+1}"
        converted_filepath = path.join(
                                        document_directory_path,
                                       f"{version_string}_{document_directory_name}.html") # Prefix indicates version

        pypandoc.convert_file(temp_save_path, 'html', outputfile=converted_filepath)
        remove(temp_save_path)

        return redirect(f"/document/{document.id}")
    return render_template('reupload.html', form=form, doc=document)



@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html', user=current_user)


@app.route("/document/<int:document_id>")
def document(document_id):
    doc = Document.query.get(document_id)
    if doc is not None:
        doc_file = codecs.open(doc.latest(), 'r', 'utf-8')
        doc_text = doc_file.read()
        doc_file.close()
        return render_template('document.html', doc=doc, doc_contents=doc_text)
    else:
        return abort(404)


@app.route("/document/<int:document_id>/delete", methods=['DELETE'])
@login_required
def delete_document(document_id):
    doc = Document.query.get(document_id)
    if doc is not None:
        if doc.author_id != current_user.id:
            return abort(401)
        else:
            db.session.delete(doc)
            db.session.commit()
            return redirect('/profile')
    else:
        return abort(404)


@app.route("/author/<int:author_id>")
def author(author_id):
    author = UserAccount.query.get(author_id)
    if author is not None:
        if author.id == current_user.id:
            return redirect("/profile")
        else:
            return render_template("author.html", author=author)
    else:
        return abort(404)


@app.route("/browse")
def browse():
    published_works = Document.query.all()
    return render_template("browse.html", works=published_works)
