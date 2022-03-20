from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import InputRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])


class PropertyForm(FlaskForm):
    title       = StringField('Title', validators=[InputRequired()])
    bathrooms   = IntegerField('Bathrooms', validators=[InputRequired()])
    rooms       = IntegerField('Rooms', validators=[InputRequired()])
    location    = StringField('Location', validators=[InputRequired()])
    price       =  IntegerField('Price', validators=[InputRequired()])
    housingtype = SelectField('type', choices=[('house', 'House'), ('apt', 'Apartment')])
    description = TextAreaField('Description', validators=[InputRequired()])
    photo       = FileField('Photo', validators=[FileRequired(), FileAllowed(['jpg', 'png'], 'Images only!') ])