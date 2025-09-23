from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,IntegerField
from wtforms.validators import Email,Length,DataRequired,ValidationError

class LoginForm(FlaskForm):
    email=StringField(label='Email',validators=[Email()])
    password=PasswordField(label='Password',validators=[Length(min=8)])
    submit=SubmitField(label='Submit')