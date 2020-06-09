from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, RadioField, TextAreaField, PasswordField, BooleanField, SubmitField, FileField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),EqualTo('password')])
    job = RadioField('Job type',choices=[('Acc','Accountant'),('Enterpu','Enterpurner')],validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    designation = StringField('Designation')
    company = StringField('Company')
    linkedin = StringField('Linked in')
    facebook = StringField('Facebook')
    twitter = StringField('Twitter')
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class AddTransactionForm(FlaskForm):
    tr_id = IntegerField('Transaction ID', validators=[DataRequired()])
    date = StringField('Date of Transaction', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0,max=140)])
    tr_type = StringField('Type of Transaction', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    file = FileField()
    submit = SubmitField('Add Transaction')

class AddCommentForm(FlaskForm):
    comment = TextAreaField('Describe', validators=[DataRequired(),Length(min=0,max=140)])
    submit = SubmitField('Comment')

class EditTransactionForm(FlaskForm):
    tr_id = IntegerField('Transaction ID', validators=[DataRequired()])
    date = StringField('Date of Transaction', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0,max=140)])
    tr_type = StringField('Type of Transaction', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])
    file = FileField()
    submit = SubmitField('Edit Transaction')

class UpdateStatusForm(FlaskForm):
    status = RadioField('Status',choices=[('True','Verified'),('False','Pending')],validators=[DataRequired()])
    submit = SubmitField('Update')