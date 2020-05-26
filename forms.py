from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from models import UserAccount, Document
from flask_login import current_user


class RegistrationForm(FlaskForm):
    display_name = StringField("Display Name", validators=[DataRequired()])
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )

    def validate_display_name(self, display_name):
        user = UserAccount.query.filter_by(
            display_name=display_name.data
        ).first()
        if user is not None:
            raise ValidationError("Please use a different display name.")

    def validate_username(self, username):
        user = UserAccount.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        user = UserAccount.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class DocumentUploadForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    document = FileField(
        validators=[
            FileRequired(),
            FileAllowed(['md', 'docx', 'rtf', 'txt', 'odt'],
                        '.md, .docx, .rtf, .txt, and .odt documents only')])

    def validate_title(self, title):
        doc = Document.query.filter_by(
            author_id=current_user.id, title=title.data).first()
        if doc is not None:
            raise ValidationError("You have already published a work with this name.")


class DocumentReuploadForm(FlaskForm):
    document = FileField(
        validators=[
            FileRequired(),
            FileAllowed(['md', 'docx', 'rtf', 'txt', 'odt'],
                        '.md, .docx, .rtf, .txt, and .odt documents only')])