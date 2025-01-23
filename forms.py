#forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class Registration(FlaskForm):
    name1=StringField('First Name  : ', validators=[DataRequired(), Length(min=3)])
    name2=StringField('Second Name : ', validators=[DataRequired()])
    uname=StringField('Username: ')
    tel=StringField('Phone    :  ', validators=[DataRequired(), Length(min=10)])
    email=StringField('Email  : ', validators=[Email()])
    password=PasswordField('Password : ',validators=[DataRequired(), Length(min=6)])
    rec_id=StringField('Rec ID : ')
    submit=SubmitField('Submit : ')
    
class Login(FlaskForm):
    uname=StringField('Name : ', validators=[DataRequired()])
    password=PasswordField('Password : ', validators=[DataRequired()])
    submit=SubmitField('LogIn')