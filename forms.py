#forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
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
    
    
class Requests(FlaskForm):
    name1=StringField('First Name', validators=[DataRequired()])
    name2=StringField('Second Name', validators=[DataRequired()])
    tel = StringField('Phone Number', validators=[DataRequired(), Length(min=10)])
    email= StringField('Email Address', validators=[Email()])
    rec_id = StringField('Recruiter ID')
    pw =PasswordField('Prefered Password', validators=[Length(min=6)])
    
    opt=SelectField('Payment Method', choices= [('Select', '--select--'), ('Airtel', 'Airtel Money'), ('MTN', 'MTN Mobile Money')], validators=[DataRequired()])
    
    txn = StringField('Transaction ID', validators=[DataRequired(), Length(min=11)])
    send=SubmitField('Submit')
    
class Auto(FlaskForm):
    id=StringField('ID', validators=[DataRequired()])
    uname=StringField('Username', validators=[DataRequired()])
    add=SubmitField('Add')
    
class Withdraw(FlaskForm):
    amm = StringField('Ammount', validators=[DataRequired()])
    name = StringField('Name Registered With your Number', validators=[DataRequired()])
    pw=PasswordField('Your Password', validators=[DataRequired()])
    submit=SubmitField('SUBMIT REQUEST')